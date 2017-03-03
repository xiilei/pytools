from subprocess import Popen,PIPE,TimeoutExpired,STDOUT
from io import StringIO

def logs(since=None,until=None):
    cmd = ['git','log','--pretty=format:%cd %h %cn %s %N','--date=short','--numstat']
    if since:
        cmd.append('--since=%s' % since)
    if end:
        cmd.append('--until=%s' % until)
    proc = Popen(cmd,stdout = PIPE,stderr=STDOUT,shell=False)
    try:
        outs,errs = proc.communicate(timeout=15)
        return StringIO(outs.decode('utf-8'))
    except TimeoutExpired as e:
        print('timeout')
        proc.kill()
        return StringIO('')

def isphpfile(file):
    return file.endswith('.php')

def isnewcommit(s):
    return len(s[0:7].replace('\t','')) == 7

def add_comments(lines,comment):
    maxadd = 0
    file  = ''
    for line in lines:
        adds,dels,f = line.split('\t')
        if int(adds) > maxadd:
            maxadd = int(adds)
            file = f
    if file:
        write_comment(pretty_comment(comment),file)

def pretty_comment(comment):
    return comment.strip()

def write_comment(comment,file):
    if not os.path.exists(file):
        print('%s not exists' % file)
        return False
    print('wirte %s to %s' % (comment,file))
    with open(file,'r+') as f:
        head = f.readline()
        content = f.read()
        f.seek(0, 0)
        f.write(head)
        f.write('//%s\n' % comment)
        f.write(content)

with logs('2016-10-01') as f:
    line = True
    filelines = []
    comment = ''
    while line:
        line = f.readline()
        if len(line) < 7:
            continue
        if isnewcommit(line):
            add_comments(filelines,comment)
            filelines = []
            comment = line
        else:
            line = line.strip('\t\n ')
            if isphpfile(line):
                filelines.append(line)



