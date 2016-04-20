"""
Unit tests for Neo module
"""
import neomodel
from django.test import TestCase
from django.test.utils import override_settings
from cl.search.models import OpinionCluster, OpinionsCited
from cl.neo.models import OpinionNode


@override_settings(

)
class NeoTestCase(TestCase):
    """ Base Neo test class """

    fixtures = ['scotus_map_data.json']

    def setUp(self):
        neomodel.db.cypher_query('MATCH (n) DETACH DELETE n')

        for oc in OpinionCluster.objects.all():
            node = OpinionNode(opinion_pk=oc.pk)
            node.case_name = oc.case_name_short
            print 'Creating node for Case: %s' % (node.case_name)
            node.save()

        for citation in OpinionsCited.objects.all():
            cited_node = OpinionNode.nodes.get(
                opinion_pk=citation.cited_opinion_id
            )
            citing_node = OpinionNode.nodes.get(
                opinion_pk=citation.citing_opinion_id
            )

            citing_node.cites.connect(cited_node)

            print '--adding citation: %s -[cites]-> %s' % \
                  (citing_node.case_name, cited_node.case_name)

            cited_node.save()
            citing_node.save()


class QuickTest(NeoTestCase):

    def test_can_load_nodes(self):
        self.assertIsNotNone(OpinionNode.nodes.get(case_name='Ball'))