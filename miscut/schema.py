import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView as GQLView

from .model import db, Conference as ConferenceModel, Event as EventModel, VideoFile as VideoFileModel, VideoSegment as VideoSegmentModel

class VideoFile(SQLAlchemyObjectType):
    id = graphene.ID(required=True)
    url = graphene.String()
    class Meta:
        model = VideoFileModel
        interfaces = (relay.Node, )


class VideoFileConnection(relay.Connection):
    class Meta:
        node = VideoFile



class VideoSegment(SQLAlchemyObjectType):
    class Meta:
        model = VideoSegmentModel
        interfaces = (relay.Node, )


class VideoSegmentConn(relay.Connection):
    class Meta:
        node = VideoSegment


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    files = SQLAlchemyConnectionField(VideoFileConnection)
    segments = SQLAlchemyConnectionField(VideoSegmentConn)

schema = graphene.Schema(query=Query)

class GraphQLView(GQLView):
    def get_context(self, request):
        context = super().get_context(request)
        context.update({'current_user': current_user})
        return context

