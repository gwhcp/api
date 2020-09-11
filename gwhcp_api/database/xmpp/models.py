from django.db import models


class Archive(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    timestamp = models.BigIntegerField()

    peer = models.TextField()

    bare_peer = models.TextField()

    xml = models.TextField()

    txt = models.TextField(
        blank=True,
        null=True
    )

    kind = models.TextField(
        blank=True,
        null=True
    )

    nick = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'archive'

        default_permissions = ()


class ArchivePrefs(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    def_field = models.TextField(
        db_column='def'
    )  # Field renamed because it was a Python reserved word.

    always = models.TextField()

    never = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'archive_prefs'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class Bosh(models.Model):
    sid = models.TextField(
        unique=True
    )

    node = models.TextField()

    pid = models.TextField()

    class Meta:
        db_table = 'bosh'

        default_permissions = ()


class CapsFeatures(models.Model):
    node = models.TextField()

    subnode = models.TextField()

    feature = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'caps_features'

        default_permissions = ()


class Last(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    seconds = models.TextField()

    state = models.TextField()

    class Meta:
        db_table = 'last'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class MixChannel(models.Model):
    channel = models.TextField()

    service = models.TextField()

    username = models.TextField()

    domain = models.TextField()

    jid = models.TextField()

    hidden = models.BooleanField()

    hmac_key = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'mix_channel'

        default_permissions = ()

        unique_together = (
            (
                'channel',
                'service'
            ),
        )


class MixPam(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    channel = models.TextField()

    service = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'mix_pam'

        default_permissions = ()

        unique_together = (
            (
                'username',
                'server_host',
                'channel',
                'service'
            ),
        )


class MixParticipant(models.Model):
    channel = models.TextField()

    service = models.TextField()

    username = models.TextField()

    domain = models.TextField()

    jid = models.TextField()

    nick = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'mix_participant'

        default_permissions = ()

        unique_together = (
            (
                'channel',
                'service',
                'username',
                'domain'
            ),
        )


class MixSubscription(models.Model):
    channel = models.TextField()

    service = models.TextField()

    username = models.TextField()

    domain = models.TextField()

    node = models.TextField()

    jid = models.TextField()

    class Meta:
        db_table = 'mix_subscription'

        default_permissions = ()

        unique_together = (
            (
                'channel',
                'service',
                'username',
                'domain',
                'node'
            ),
        )


class Motd(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    xml = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'motd'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class MqttPub(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    resource = models.TextField()

    topic = models.TextField()

    qos = models.SmallIntegerField()

    payload = models.BinaryField()

    payload_format = models.SmallIntegerField()

    content_type = models.TextField()

    response_topic = models.TextField()

    correlation_data = models.BinaryField()

    user_properties = models.BinaryField()

    expiry = models.BigIntegerField()

    class Meta:
        db_table = 'mqtt_pub'

        default_permissions = ()

        unique_together = (
            (
                'topic',
                'server_host'
            ),
        )


class MucOnlineRoom(models.Model):
    name = models.TextField()

    host = models.TextField()

    server_host = models.TextField()

    node = models.TextField()

    pid = models.TextField()

    class Meta:
        db_table = 'muc_online_room'

        default_permissions = ()

        unique_together = (
            (
                'name',
                'host'
            ),
        )


class MucOnlineUsers(models.Model):
    username = models.TextField()

    server = models.TextField()

    resource = models.TextField()

    name = models.TextField()

    host = models.TextField()

    server_host = models.TextField()

    node = models.TextField()

    class Meta:
        db_table = 'muc_online_users'

        default_permissions = ()

        unique_together = (
            (
                'username',
                'server',
                'resource',
                'name',
                'host'
            ),
        )


class MucRegistered(models.Model):
    jid = models.TextField()

    host = models.TextField()

    server_host = models.TextField()

    nick = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'muc_registered'

        default_permissions = ()

        unique_together = (
            (
                'jid',
                'host'
            ),
        )


class MucRoom(models.Model):
    name = models.TextField()

    host = models.TextField()

    server_host = models.TextField()

    opts = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'muc_room'

        default_permissions = ()

        unique_together = (
            (
                'name',
                'host'
            ),
        )


class MucRoomSubscribers(models.Model):
    room = models.TextField()

    host = models.TextField()

    jid = models.TextField()

    nick = models.TextField()

    nodes = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'muc_room_subscribers'

        default_permissions = ()

        unique_together = (
            (
                'host',
                'room',
                'jid'
            ),
        )


class OauthClient(models.Model):
    client_id = models.TextField(
        primary_key=True
    )

    client_name = models.TextField()

    grant_type = models.TextField()

    options = models.TextField()

    class Meta:
        db_table = 'oauth_client'

        default_permissions = ()


class OauthToken(models.Model):
    token = models.TextField(
        unique=True
    )

    jid = models.TextField()

    scope = models.TextField()

    expire = models.BigIntegerField()

    class Meta:
        db_table = 'oauth_token'

        default_permissions = ()


class PrivacyDefaultList(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    name = models.TextField()

    class Meta:
        db_table = 'privacy_default_list'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class PrivacyList(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    name = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'privacy_list'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username',
                'name'
            ),
        )


class PrivacyListData(models.Model):
    autoid = models.AutoField(
        primary_key=True
    )

    id = models.ForeignKey(
        PrivacyList,
        models.DO_NOTHING,
        db_column='id',
        blank=True,
        null=True
    )

    t = models.CharField(
        max_length=1
    )

    value = models.TextField()

    action = models.CharField(
        max_length=1
    )

    ord = models.DecimalField(
        max_digits=1000,
        decimal_places=1000
    )

    match_all = models.BooleanField()

    match_iq = models.BooleanField()

    match_message = models.BooleanField()

    match_presence_in = models.BooleanField()

    match_presence_out = models.BooleanField()

    class Meta:
        db_table = 'privacy_list_data'

        default_permissions = ()


class PrivateStorage(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    namespace = models.TextField()

    data = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'private_storage'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username',
                'namespace'
            ),
        )


class Proxy65(models.Model):
    sid = models.TextField(
        unique=True
    )

    pid_t = models.TextField()

    pid_i = models.TextField()

    node_t = models.TextField()

    node_i = models.TextField()

    jid_i = models.TextField()

    class Meta:
        db_table = 'proxy65'

        default_permissions = ()


class PubsubItem(models.Model):
    nodeid = models.ForeignKey(
        'PubsubNode',
        models.DO_NOTHING,
        db_column='nodeid',
        blank=True,
        null=True
    )

    itemid = models.TextField()

    publisher = models.TextField()

    creation = models.CharField(max_length=32)

    modification = models.CharField(max_length=32)

    payload = models.TextField()

    class Meta:
        db_table = 'pubsub_item'

        default_permissions = ()

        unique_together = (
            (
                'nodeid',
                'itemid'
            ),
        )


class PubsubNode(models.Model):
    host = models.TextField()

    node = models.TextField()

    parent = models.TextField()

    plugin = models.TextField()

    nodeid = models.AutoField(
        unique=True,
        primary_key=True
    )

    class Meta:
        db_table = 'pubsub_node'

        default_permissions = ()

        unique_together = (
            (
                'host',
                'node'
            ),
        )


class PubsubNodeOption(models.Model):
    nodeid = models.ForeignKey(
        PubsubNode,
        models.DO_NOTHING,
        db_column='nodeid',
        blank=True,
        null=True
    )

    name = models.TextField()

    val = models.TextField()

    class Meta:
        db_table = 'pubsub_node_option'

        default_permissions = ()


class PubsubNodeOwner(models.Model):
    nodeid = models.ForeignKey(
        PubsubNode,
        models.DO_NOTHING,
        db_column='nodeid',
        blank=True,
        null=True
    )

    owner = models.TextField()

    class Meta:
        db_table = 'pubsub_node_owner'

        default_permissions = ()


class PubsubState(models.Model):
    nodeid = models.ForeignKey(
        PubsubNode,
        models.DO_NOTHING,
        db_column='nodeid',
        blank=True,
        null=True
    )

    jid = models.TextField()

    affiliation = models.CharField(
        max_length=1,
        blank=True,
        null=True
    )

    subscriptions = models.TextField()

    stateid = models.AutoField(
        unique=True,
        primary_key=True
    )

    class Meta:
        db_table = 'pubsub_state'

        default_permissions = ()

        unique_together = (
            (
                'nodeid',
                'jid'
            ),
        )


class PubsubSubscriptionOpt(models.Model):
    subid = models.TextField()

    opt_name = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )

    opt_value = models.TextField()

    class Meta:
        db_table = 'pubsub_subscription_opt'

        default_permissions = ()

        unique_together = (
            (
                'subid',
                'opt_name'
            ),
        )


class PushSession(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    timestamp = models.BigIntegerField()

    service = models.TextField()

    node = models.TextField()

    xml = models.TextField()

    class Meta:
        db_table = 'push_session'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username',
                'timestamp'
            ),
            (
                'server_host',
                'username',
                'service',
                'node'
            ),
        )


class RosterVersion(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    version = models.TextField()

    class Meta:
        db_table = 'roster_version'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class Rostergroups(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    jid = models.TextField()

    grp = models.TextField()

    class Meta:
        db_table = 'rostergroups'

        default_permissions = ()


class Rosterusers(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    jid = models.TextField()

    nick = models.TextField()

    subscription = models.CharField(
        max_length=1
    )

    ask = models.CharField(
        max_length=1
    )

    askmessage = models.TextField()

    server = models.CharField(
        max_length=1
    )

    subscribe = models.TextField()

    type = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'rosterusers'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username',
                'jid'
            ),
        )


class Route(models.Model):
    domain = models.TextField()

    server_host = models.TextField()

    node = models.TextField()

    pid = models.TextField()

    local_hint = models.TextField()

    class Meta:
        db_table = 'route'

        default_permissions = ()

        unique_together = (
            (
                'domain',
                'server_host',
                'node',
                'pid'
            ),
        )


class Sm(models.Model):
    usec = models.BigIntegerField(
        primary_key=True
    )

    pid = models.TextField()

    node = models.TextField()

    username = models.TextField()

    server_host = models.TextField()

    resource = models.TextField()

    priority = models.TextField()

    info = models.TextField()

    class Meta:
        db_table = 'sm'

        default_permissions = ()

        unique_together = (
            (
                'usec',
                'pid'
            ),
        )


class Spool(models.Model):
    username = models.TextField()

    server_host = models.TextField()

    xml = models.TextField()

    seq = models.AutoField(
        primary_key=True
    )

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'spool'

        default_permissions = ()


class SrGroup(models.Model):
    name = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    opts = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'sr_group'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'name'
            ),
        )


class SrUser(models.Model):
    jid = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    grp = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'sr_user'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'jid',
                'grp'
            ),
        )


class Users(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    password = models.TextField()

    serverkey = models.TextField()

    salt = models.TextField()

    iterationcount = models.IntegerField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class Vcard(models.Model):
    username = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    vcard = models.TextField()

    created_at = models.DateTimeField()

    class Meta:
        db_table = 'vcard'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )


class VcardSearch(models.Model):
    username = models.TextField()

    lusername = models.TextField()

    server_host = models.TextField(
        primary_key=True
    )

    fn = models.TextField()

    lfn = models.TextField()

    family = models.TextField()

    lfamily = models.TextField()

    given = models.TextField()

    lgiven = models.TextField()

    middle = models.TextField()

    lmiddle = models.TextField()

    nickname = models.TextField()

    lnickname = models.TextField()

    bday = models.TextField()

    lbday = models.TextField()

    ctry = models.TextField()

    lctry = models.TextField()

    locality = models.TextField()

    llocality = models.TextField()

    email = models.TextField()

    lemail = models.TextField()

    orgname = models.TextField()

    lorgname = models.TextField()

    orgunit = models.TextField()

    lorgunit = models.TextField()

    class Meta:
        db_table = 'vcard_search'

        default_permissions = ()

        unique_together = (
            (
                'server_host',
                'username'
            ),
        )
