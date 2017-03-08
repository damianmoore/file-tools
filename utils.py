from hashlib import md5
import os
from subprocess import Popen, PIPE
from StringIO import StringIO

from PIL import Image


def get_console_width():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def format_output(msg, columns):
    return '%s%s' % (msg, ' ' * (columns - len(msg)))


def run_cmd(cmd):
    components = []
    current_word = []
    in_quoted = False
    for char in cmd:
        if not in_quoted:
            if char == ' ':
                components.append(''.join(current_word))
                current_word = []
            elif char != '"':
                current_word.append(char)
        elif char != '"':
            current_word.append(char)
        if char == '"':
            in_quoted = not in_quoted
    components.append(''.join(current_word))
    p = Popen(components, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return p.communicate()[0]


class FileHashCache(object):
    '''
    Used with determine_same_file() function. Can keep hold of the previously
    opened orig and dest file contents. Can keep hold of all file-based and
    image-based hashes per file.
    '''
    file_hash_cache = {}
    file_data = {'orig': (None, None), 'dest': (None, None)}

    def reset(self):
        self.file_hash_cache = {}

    def get_file_hash(self, fn, hash_type):
        if fn in self.file_hash_cache and hash_type in self.file_hash_cache[fn]:
            return self.file_hash_cache[fn][hash_type]
        return None

    def set_file_hash(self, fn, hash_type, hash_val):
        if fn not in self.file_hash_cache:
            self.file_hash_cache[fn] = {}
        self.file_hash_cache[fn][hash_type] = hash_val

    def get_file(self, fn, file_type):
        if self.file_data[file_type][0] != fn:
            self.file_data[file_type] = (fn, open(fn, 'rb').read())
        return self.file_data[file_type][1]


def determine_same_file(origpath, destpath, fhc=None):
    '''
    First check if hashes of the two files match. If they don't match, they
    could still be the same image if metadata has changed so open the pixel
    data using PIL and compare hashes of that.
    '''
    if not fhc:
        fhc = FileHashCache()

    if len(fhc.file_hash_cache) > 1000:
        fhc.reset()

    orig_hash = fhc.get_file_hash(origpath, 'file')
    if not orig_hash:
        orig_hash = md5(fhc.get_file(origpath, 'orig')).hexdigest()
        fhc.set_file_hash(origpath, 'file', orig_hash)

    dest_hash = fhc.get_file_hash(destpath, 'file')
    if not dest_hash:
        dest_hash = md5(fhc.get_file(destpath, 'dest')).hexdigest()
        fhc.set_file_hash(destpath, 'file', dest_hash)

    if orig_hash == dest_hash:
        return True

    # Try matching on image data (ignoring EXIF)
    if os.path.splitext(origpath)[1][1:].lower() in ['jpg', 'jpeg', 'png', ]:
        orig_hash = fhc.get_file_hash(origpath, 'image')
        if not orig_hash:
            orig_hash = md5(Image.open(StringIO(fhc.get_file(origpath, 'orig'))).tobytes()).hexdigest()
            fhc.set_file_hash(origpath, 'image', orig_hash)

        dest_hash = fhc.get_file_hash(destpath, 'image')
        if not dest_hash:
            dest_hash = md5(Image.open(StringIO(fhc.get_file(destpath, 'dest'))).tobytes()).hexdigest()
            fhc.set_file_hash(destpath, 'image', dest_hash)

        if orig_hash == dest_hash:
            return True
    # TODO: Convert raw photos into temp jpgs to do proper comparison
    return False
