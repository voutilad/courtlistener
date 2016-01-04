"""
Unit tests for validating Fixture loading works with model logic
"""
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from cl.audio.models import Audio
from cl.judges.models import Judge
import os

class FixtureTest(TestCase):
    """Used to validate certain aspects of various fixture files...
    ...mostly that they will properly load and support other tests."""

    fixtures = ['judge_judy.json']

    def test_does_judge_judy_fixture_load(self):
        """Can we load Judge Judy from a fixture?"""
        judge = Judge.objects.get(pk=1)
        self.assertEqual(judge.name_first, 'Judith')
        self.assertEqual(judge.name_last, 'Sheindlin')


@override_settings(
    MEDIA_ROOT = os.path.join(settings.INSTALL_ROOT, 'cl/assets/media/test/')
)
class AudioFixtureTest(TestCase):

    fixtures = ['test_court.json', 'judge_judy.json', 'functest_opinions.json',
        'functest_audio.json']

    def test_calling_size_attr_on_audio_file(self):
        audio = Audio.objects.get(pk=10)
        # self.file_size_mp3 = deepgetattr(item, 'local_path_mp3.size', None)
        local_path_mp3 = audio.local_path_mp3
        print 'MEDIA_ROOT: %s' % (settings.MEDIA_ROOT,)
        print 'path: %s' % (getattr(local_path_mp3, 'path'))

        try:
            print 'size: %s' % (getattr(local_path_mp3, 'size'))
        except OSError:
            self.fail('size attribute cannot be called on local_path_mp3')
