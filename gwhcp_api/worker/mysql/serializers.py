import os

from django.contrib.auth import password_validation
from django.template.loader import render_to_string
from rest_framework import serializers

from worker.mysql.path import MysqlPath


class CreateDatabaseSerializer(serializers.Serializer):
    database = serializers.RegexField(
        help_text='Database name.',
        label='Database',
        max_length=64,
        min_length=1,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_database(self, value):
        if os.path.exists(f"{MysqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL Database '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        # Create Database
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e CREATE DATABASE {validated_database}"
            f" DEFAULT CHARACTER SET = 'utf8' COLLATE = 'utf8_general_ci';"
        )

        # Touch File
        os.mknod(f"{MysqlPath.database_dir()}{validated_database}", 0o644)

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
        if os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' currently exists.",
                code='exists'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_password = validated_data['password']

        # Create User
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e CREATE USER '{validated_user}'@'%' IDENTIFIED BY '{validated_password}';")

        # Touch File
        os.mknod(f"{MysqlPath.user_dir()}{validated_user}", 0o644)

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
        if not os.path.exists(f"{MysqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        # Drop Database
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e DROP DATABSE IF EXISTS {validated_database};"
        )

        # Remove File
        path = f"{MysqlPath.database_dir()}{validated_database}"

        if os.path.exists(path):
            os.remove(path)

        return validated_data


class DeleteUserSerializer(serializers.Serializer):
    user = serializers.RegexField(
        help_text='Username.',
        label='User',
        max_length=32,
        min_length=2,
        regex='^[a-z][a-z0-9_]+$',
        required=True
    )

    def validate_user(self, value):
        if not os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        # Drop User
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e DROP USER '{validated_user}'@'%';"
        )

        # Remove File
        path = f"{MysqlPath.user_dir()}{validated_user}"

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

    def validate_database(self, value):
        if not os.path.exists(f"{MysqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        # Revoke User Permissions
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e REVOKE ALL PRIVILEGES ON {validated_database}.* FROM '{validated_user}'@'%';"
        )

        # Grant Usage
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e GRANT usage ON {validated_database}.* TO '{validated_user}'@'%';"
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

    permission = serializers.MultipleChoiceField(
        choices=[
            'select',
            'insert',
            'update',
            'delete',
            'create',
            'alter',
            'drop',
            'index',
            'create_view',
            'show_view'
        ],
        help_text='Choose which permissions are allowed to be used.',
        label='Permission',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{MysqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_permission = validated_data['permission']

        # Revoke User Permissions
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e REVOKE ALL PRIVILEGES ON {validated_database}.* FROM '{validated_user}'@'%';"
        )

        # Grant Usage
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e GRANT usage ON {validated_database}.* TO '{validated_user}'@'%';"
        )

        # Set Permission(s)
        permission = ''

        for item in validated_permission:
            permission += f"{item},"

        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e GRANT {permission[:-1]} ON {validated_database}.* TO '{validated_user}'@'%';"
        )

        return validated_data


class PasswordSerializer(serializers.Serializer):
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
        if not os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_intalled'
            )

        return attrs

    def create(self, validated_data):
        validated_user = validated_data['user']

        validated_password = validated_data['password']

        # Update User Password
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e SET PASSWORD FOR '{validated_user}'@'%' = PASSWORD('{validated_password}');"
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

    permission = serializers.MultipleChoiceField(
        choices=[
            'select',
            'insert',
            'update',
            'delete',
            'create',
            'alter',
            'drop',
            'index',
            'create_view',
            'show_view'
        ],
        help_text='Choose which permissions are allowed to be used.',
        label='Permission',
        required=True
    )

    def validate_database(self, value):
        if not os.path.exists(f"{MysqlPath.database_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL Database '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate_user(self, value):
        if not os.path.exists(f"{MysqlPath.user_dir()}{value}"):
            raise serializers.ValidationError(
                f"MySQL User '{value}' does not exist.",
                code='not_found'
            )

        return value

    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        validated_database = validated_data['database']

        validated_user = validated_data['user']

        validated_permission = validated_data['permission']

        # Revoke User Permissions
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e REVOKE ALL PRIVILEGES ON {validated_database}.* FROM '{validated_user}'@'%';"
        )

        # Grant Usage
        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e GRANT usage ON {validated_database}.* TO '{validated_user}'@'%';"
        )

        # Set Permission(s)
        permission = ''

        for item in validated_permission:
            permission += f"{item},"

        os.system(
            f"{MysqlPath.mysql_cmd()}"
            f" -e GRANT {permission[:-1]} ON {validated_database}.* TO '{validated_user}'@'%';"
        )

        return validated_data


class ServerInstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has already been installed.',
                code='installed'
            )

        return attrs

    def create(self, validated_data):
        # If path does not exist, create it
        if not os.path.exists(MysqlPath.database_dir()):
            os.makedirs(MysqlPath.database_dir(), 0o755)

        if not os.path.exists(MysqlPath.user_dir()):
            os.makedirs(MysqlPath.user_dir(), 0o755)

        # Setup MySQL if not already done
        if not os.listdir(MysqlPath.varlib_dir()):
            os.system(
                f"{MysqlPath.mysql_install_db_cmd()}"
                f" --user=mysql"
                f" --basedir/usr"
                f" --datadir={MysqlPath.varlib_dir()}"
                f" >/dev/null 2>&1"
            )

        # Removing existing configuration
        path_my = f"{MysqlPath.conf_dir()}my.cnf"

        if os.path.exists(path_my):
            os.remove(path_my)

        content = render_to_string('mysql/my.cnf.tmpl') \
            .replace('[MYSQL-RUN]', MysqlPath.run_dir()) \
            .replace('[MYSQL-VARLIB]', MysqlPath.varlib_dir())

        handle = open(path_my, 'w')
        handle.write(content)
        handle.close()

        os.mknod(f"{MysqlPath.conf_dir()}.isInstalled", 0o644)

        return validated_data


class ServerUninstallSerializer(serializers.Serializer):
    def validate(self, attrs):
        if not os.path.exists(f"{MysqlPath.conf_dir()}.isInstalled"):
            raise serializers.ValidationError(
                'MySQL Server has not yet been installed.',
                code='not_installed'
            )

        return attrs

    def create(self, validated_data):
        config_file = f"{MysqlPath.conf_dir()}my.cnf"

        if os.path.exists(config_file):
            os.remove(config_file)

        os.remove(f"{MysqlPath.conf_dir()}.isInstalled")

        return validated_data
