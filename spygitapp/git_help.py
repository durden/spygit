import os
import tempfile


def git_clone(url):
    """Clone git project in a temporary directory
        Returns: Directory project cloned in
    """

    tmp_path = tempfile.mkdtemp(prefix='spygit-')

    st = os.system("cd %s && git clone %s" % (tmp_path, url))
    if st != 0:
        os.system("\rm -fr %s" % (tmp_path))
        raise Exception("Unable to find project, please check git url")

    # get the project name from the top level directory
    git_name = os.listdir(tmp_path)[0]
    git_path = tmp_path + '/' + git_name

    return git_path, git_name


def git_head_revision(proj_path):
    """Get the HEAD revision of given project"""

    # FIXME: Not very good should probably look for specific exceptions here
    try:
        gpipe = os.popen("cd %s && git --no-pager log --max-count=1" % proj_path)
        rev = gpipe.readlines()[0].replace('commit ', '', 1)
        rev = rev.strip('\n')
        gpipe.close()
    except:
        raise Exception("Unable to find HEAD revision for project, "
                        "please check project")

    return rev
