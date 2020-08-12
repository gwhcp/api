import os

from django.contrib.auth import password_validation
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.postgresql.path import PostgresqlPath
from worker.system.path import SystemPath


class CreateDatabaseSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_database(self, value):
        if os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate_user(self, value):
        if os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        #
        # Template1 Specific
        #

        # Create Database
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c CREATE DATABASE {validated_database}"
            f" >/dev/null 2>&1"
        )

        # Revoke Database Permissions
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c REVOKE ALL ON DATABASE {validated_database} FROM public;"
            f" >/dev/null 2>&1"
        )

        # Grant Database Connection Permission
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c GRANT connect ON DATABASE {validated_database} TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        #
        # Database Specific
        #

        # Set Search Path
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c SET search_path = public;"
            f" >/dev/null 2>&1"
        )

        # Set Role Search Path
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER ROLE {validated_user} IN DATABASE {validated_database} SET search_path  = public;"
            f" >/dev/null 2>&1"
        )

        # Grant Schema Permissions
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c GRANT usage, create ON SCHEMA public TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Touch Files
        os.mknod(f"{PostgresqlPath.database_dir()}{validated_database}", 0o644)

        return validated_data


class CreateUserSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    password = serializers.CharField(
        help_text='Password.',
        label='Password',
        max_length=72,
        required=True,
        validators=[
            password_validation.validate_password
        ]
    )

    def validate_user(self, value):
        if os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_password = validated_data['password']

        #
        # Template1 Specific
        #

        # Create Role
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c CREATE ROLE {validated_user}"
            f" NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ENCRYPTED PASSWORD '{validated_password}';"
            f" >/dev/null 2>&1"
        )

        # Touch File
        os.mknod(f"{PostgresqlPath.user_dir()}{validated_user}", 0o644)

        return validated_data


class DeleteDatabaseSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        #
        # Template1 Specific
        #

        # Drop Database
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c DROP DATABASE IF EXISTS {validated_database};"
            f" >/dev/null 2>&1"
        )

        # Remove File
        path = f"{PostgresqlPath.database_dir()}{validated_database}"

        if os.path.exists(path):
            os.remove(path)

        return validated_data


class DeleteUserSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    owner = serializers.RegexField(
        help_text='Username of database owner.',
        label='Owner',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_owner(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Owner '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_owner = validated_data['owner']

        #
        # Template1 Specific
        #

        # Reassign Owned Data
        if validated_owner != validated_user:
            os.system(
                f"{PostgresqlPath.psql_cmd()}"
                f" -U postgres"
                f" -d {validated_database}"
                f" -c REASSIGN OWNED BY {validated_user} TO {validated_owner};"
                f" >/dev/null 2>&1"
            )

        # Drop Owned
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c DROP OWNED BY {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Drop Role
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c DROP ROLE {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Remove File
        path = f"{PostgresqlPath.user_dir()}{validated_user}"

        if os.path.exists(path):
            os.remove(path)

        return validated_data


class DisableSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    owner = serializers.RegexField(
        help_text='Username of database owner.',
        label='Owner',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_owner(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Owner '{value}' does not exist."
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_owner = validated_data['owner']

        #
        # Template1 Specific
        #

        # Revoke Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Table Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON TABLES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Sequence Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON SEQUENCES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        return validated_data


class EnableSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    owner = serializers.RegexField(
        help_text='Username of database owner.',
        label='Owner',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    permission = serializers.MultipleChoiceField(
        choices=[
            'select',
            'insert',
            'update',
            'delete',
            'truncate',
            'references',
            'trigger'
        ],
        help_text='Choose which permissions are allowed to be used.',
        label='Permission',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_owner(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Owner '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_owner = validated_data['owner']

        validated_permission = validated_data['permission']

        #
        # Template1 Specific
        #

        # Revoke Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {validated_user};"
            f"  >/dev/null 2>&1"
        )

        # Revoke Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Table Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON TABLES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Sequence Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON SEQUENCES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Set Permission(s)
        table_permission = ''

        for item in validated_permission:
            table_permission += f"{item},"

        # Grant Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c GRANT {table_permission[:-1]} ON ALL TABLES IN SCHEMA public TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Alter Default Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public GRANT {table_permission[:-1]} ON TABLES TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        sequence_permission = 'usage,'

        if 'select' in validated_permission:
            sequence_permission += 'select,'

        if 'update' in validated_permission:
            sequence_permission += 'update,'

        # Grant Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c GRANT {table_permission[:-1]} ON ALL SEQUENCES IN SCHEMA public TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Alter Default Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public GRANT {table_permission[:-1]} ON SEQUENCES TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        return validated_data


class PasswordSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=16,
        min_length=3,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    password = serializers.CharField(
        help_text='Password.',
        label='Password',
        max_length=72,
        required=True,
        validators=[
            password_validation.validate_password
        ]
    )

    def validate_user(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_password = validated_data['password']

        #
        # Template1 Specific
        #

        # Alter Role
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -c ALTER ROLE {validated_user} WITH ENCRYPTED PASSWORD '{validated_password}';"
            f" >/dev/null 2>&1"
        )

        return validated_data


class PermissionSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    owner = serializers.RegexField(
        help_text='Username of database owner.',
        label='Owner',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    permission = serializers.MultipleChoiceField(
        choices=[
            'select',
            'insert',
            'update',
            'delete',
            'truncate',
            'references',
            'trigger'
        ],
        help_text='Choose which permissions are allowed to be used.',
        label='Permission',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{PostgresqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_owner(self, value):
        if not os.path.exists(f"{PostgresqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"PostgreSQL Owner '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_owner = validated_data['owner']

        validated_permission = validated_data['permission']

        #
        # Template1 Specific
        #

        # Revoke Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Table Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON TABLES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Revoke Default Sequence Permissions(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public REVOKE ALL PRIVILEGES ON SEQUENCES FROM {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Set Permission(s)
        table_permission = ''

        for item in validated_permission:
            table_permission += f"{item},"

        # Grant Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c GRANT {table_permission[:-1]} ON ALL TABLES IN SCHEMA public TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Alter Default Table Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public GRANT {table_permission[:-1]} ON TABLES TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        sequence_permission = 'usage,'

        if 'select' in validated_permission:
            sequence_permission += 'select,'

        if 'update' in validated_permission:
            sequence_permission += 'update,'

        # Grant Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c GRANT {table_permission[:-1]} ON ALL SEQUENCES IN SCHEMA public TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        # Alter Default Sequence Permission(s)
        os.system(
            f"{PostgresqlPath.psql_cmd()}"
            f" -U postgres"
            f" -d {validated_database}"
            f" -c ALTER DEFAULT PRIVILEGES FOR ROLE {validated_owner}"
            f" IN SCHEMA public GRANT {table_permission[:-1]} ON SEQUENCES TO {validated_user};"
            f" >/dev/null 2>&1"
        )

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(PostgresqlPath.database_dir()):
            os.makedirs(PostgresqlPath.database_dir(), 0o755)

        if not os.path.exists(PostgresqlPath.user_dir()):
            os.makedirs(PostgresqlPath.user_dir(), 0o755)

        if not os.path.exists(PostgresqlPath.archive_dir()):
            os.makedirs(PostgresqlPath.archive_dir(), 0o755)

        # Setup PostgreSQL if not already done
        if not os.listdir(PostgresqlPath.data_dir()):
            os.system(
                f"{SystemPath.su_cmd()}"
                f" -c {PostgresqlPath.initdb_cmd()}"
                f" --locale $LANG -E UTF8 -D '{PostgresqlPath.data_dir()}' postgres"
                f" >/dev/null 2>&1"
            )

        # pg_hba.conf
        path_pg_hba = f"{PostgresqlPath.data_dir()}pg_hba.conf"

        if os.path.exists(path_pg_hba):
            os.remove(path_pg_hba)

        handle = open(path_pg_hba, 'w')
        handle.write(render_to_string('postgresql/pg_hba.conf.tmpl'))
        handle.close()

        # postgresql.conf
        path_postgresql = f"{PostgresqlPath.data_dir()}postgresql.conf"

        if os.path.exists(path_postgresql):
            os.remove(path_postgresql)

        content_postgresql = render_to_string('postgresql/postgresql.conf.tmpl') \
            .replace('[POSTGRESQL-RUN]', PostgresqlPath.run_dir()) \
            .replace('[POSTGRESQL-ARCHIVE]', PostgresqlPath.archive_dir())

        handle2 = open(path_postgresql, 'w')
        handle2.write(content_postgresql)
        handle2.close()

        # recovery.conf
        path_recovery = f"{PostgresqlPath.data_dir()}recovery.conf.dist"

        if os.path.exists(path_recovery):
            os.remove(path_recovery)

        content_recovery = render_to_string('postgresql/recovery.conf.tmpl') \
            .replace('[POSTGRESQL-ARCHIVE]', PostgresqlPath.archive_dir())

        handle3 = open(path_recovery, 'w')
        handle3.write(content_recovery)
        handle3.close()

        os.mknod(f"{PostgresqlPath.data_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{PostgresqlPath.data_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'PostgreSQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(PostgresqlPath.database_dir()):
            os.makedirs(PostgresqlPath.database_dir(), 0o755)

        if not os.path.exists(PostgresqlPath.user_dir()):
            os.makedirs(PostgresqlPath.user_dir(), 0o755)

        if not os.path.exists(PostgresqlPath.archive_dir()):
            os.makedirs(PostgresqlPath.archive_dir(), 0o755)

        # pg_hba.conf
        path_pg_hba = f"{PostgresqlPath.data_dir()}pg_hba.conf"

        if os.path.exists(path_pg_hba):
            os.remove(path_pg_hba)

        # postgresql.conf
        path_postgresql = f"{PostgresqlPath.data_dir()}postgresql.conf"

        if os.path.exists(path_postgresql):
            os.remove(path_postgresql)

        # recovery.conf
        path_recovery = f"{PostgresqlPath.data_dir()}recovery.conf.dist"

        if os.path.exists(path_recovery):
            os.remove(path_recovery)

        os.remove(f"{PostgresqlPath.data_dir()}.isInstalled")

        return validated_data
