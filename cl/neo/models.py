"""
    Graph models
"""

from neomodel import (
    StructuredNode, StringProperty, IntegerProperty, RelationshipTo,
    RelationshipFrom
)


class OpinionNode(StructuredNode):
    """ Maps to a Court Opinion """

    case_name = StringProperty(index=True)
    opinion_pk = IntegerProperty(unique_index=True, required=True)
    cited_by = RelationshipFrom('OpinionNode', 'CITED_BY')
    cites = RelationshipTo('OpinionNode', 'CITES')