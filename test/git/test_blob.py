import time
from test.testlib import *
from git_python import *

class TestBlob(object):
    def setup(self):
        self.repo = Repo(GIT_REPO)
    
    @patch(Git, 'method_missing')
    def test_should_return_blob_contents(self, git):
        git.return_value = fixture('cat_file_blob')
        blob = Blob(self.repo, **{'id': 'abc'})
        assert_equal("Hello world", blob.data)
        assert_true(git.called)
        assert_equal(git.call_args, (('cat_file', 'abc'), {'p': True}))
    
    @patch(Git, 'method_missing')
    def test_should_cache_data(self, git):
        git.return_value = fixture('cat_file_blob')
        blob = Blob(self.repo, **{'id': 'abc'})
        blob.data
        blob.data
        assert_true(git.called)
        assert_equal(git.call_count, 1)
        assert_equal(git.call_args, (('cat_file', 'abc'), {'p': True}))

    @patch(Git, 'method_missing')
    def test_should_return_file_size(self, git):
        git.return_value = fixture('cat_file_blob_size')
        blob = Blob(self.repo, **{'id': 'abc'})
        assert_equal(11, blob.size)
        assert_true(git.called)
        assert_equal(git.call_args, (('cat_file', 'abc'), {'s': True}))

    @patch(Git, 'method_missing')
    def test_should_cache_file_size(self, git):
        git.return_value = fixture('cat_file_blob_size')
        blob = Blob(self.repo, **{'id': 'abc'})
        assert_equal(11, blob.size)
        assert_equal(11, blob.size)        
        assert_true(git.called)
        assert_equal(git.call_count, 1)
        assert_equal(git.call_args, (('cat_file', 'abc'), {'s': True}))
  
    def test_mime_type_should_return_mime_type_for_known_types(self):
        blob = Blob(self.repo, **{'id': 'abc', 'name': 'foo.png'})
        assert_equal("image/png", blob.mime_type)
  
    def test_mime_type_should_return_text_plain_for_unknown_types(self):
        blob = Blob(self.repo, **{'id': 'abc'})
        assert_equal("text/plain", blob.mime_type)
  
    @patch(Git, 'method_missing')
    def test_should_display_blame_information(self, git):
        git.return_value = fixture('blame')
        b = Blob.blame(self.repo, 'master', 'lib/git.py')
        assert_equal(13, len(b))
        # assert_equal(25, reduce(lambda acc, x: acc + len(x[-1]), b))
        assert_equal(hash(b[0][0]), hash(b[9][0]))
        c = b[0][0]
        assert_true(git.called)
        assert_equal(git.call_args, (('blame', 'master', '--', 'lib/git.py'), {'p': True}))
        
        assert_equal('634396b2f541a9f2d58b00be1a07f0c358b999b3', c.id)
        assert_equal('Tom Preston-Werner', c.author.name)
        assert_equal('tom@mojombo.com', c.author.email)
        assert_equal(time.gmtime(1191997100), c.authored_date)
        assert_equal('Tom Preston-Werner', c.committer.name)
        assert_equal('tom@mojombo.com', c.committer.email)
        assert_equal(time.gmtime(1191997100), c.committed_date)
        assert_equal('initial grit setup', c.message)
  
    def test_should_return_appropriate_representation(self):
        blob = Blob(self.repo, **{'id': 'abc'})
        assert_equal('<GitPython.Blob "abc">', repr(blob))
