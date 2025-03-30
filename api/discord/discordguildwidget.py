# coding: utf-8

from typing import List

from marshmallow import Schema, fields


class DiscordGuildWidgetSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    invite_link = fields.Str()
    member_count = fields.Int()
    members = fields.List(fields.Nested('DiscordGuildWidgetMemberSchema'))


class DiscordGuildWidgetMemberSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    status = fields.Str()
    avatar = fields.Str()
    avatar_url = fields.Str()


class DiscordGuildWidgetMember(object):

    def __init__(self, id: str, username: str, status: str, avatar: str):
        self.id = id
        self.username = username
        self.avatar = avatar
        self.status = status


class DiscordGuildWidget(object):

    def __init__(self, id: str, name: str, invite_link: str, member_count: int, members: List[DiscordGuildWidgetMember] = None):
        self.id = id
        self.name = name
        self.invite_link = invite_link
        self.member_count = member_count
        self.members = members if members is not None else []
