#!/usr/bin/env python3
"""Real terminal smoke checks; never touches student files or shell history."""
import fcntl
import os
from pathlib import Path
import pty
import select
import signal
import struct
import tempfile
import termios
import time


class Session:
    def __init__(self, command, cwd):
        pid, fd = pty.fork()
        if pid == 0:
            os.chdir(cwd)
            env = dict(os.environ, TERM='xterm', LANG='C', LC_ALL='C', HISTFILE='/dev/null', PS1='LAB2_PROMPT> ', PROMPT_COMMAND='')
            os.execvpe(command[0],command,env)
        self.pid, self.fd = pid, fd
        fcntl.ioctl(fd,termios.TIOCSWINSZ,struct.pack('HHHH',30,100,0,0))

    def send(self, data):
        os.write(self.fd,data)

    def until(self, needle, timeout=8):
        data=b''
        deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            if select.select([self.fd],[],[],0.1)[0]:
                try:
                    part=os.read(self.fd,65536)
                except OSError:
                    break
                if not part:
                    break
                data+=part
                if needle in data:
                    return data
        raise AssertionError(f'Terminal did not show {needle!r}: {data[-1500:]!r}')

    def close(self):
        try:
            os.kill(self.pid,signal.SIGKILL)
        except ProcessLookupError:
            pass
        os.close(self.fd)
        os.waitpid(self.pid,0)


def main():
    with tempfile.TemporaryDirectory(prefix='lab2-interactive-') as folder:
        shell=Session(['bash','--noprofile','--norc','-i'],folder)
        try:
            shell.until(b'LAB2_PROMPT> ')
            shell.send(b'echo HISTORY_OLDER\r'); shell.until(b'LAB2_PROMPT> ')
            shell.send(b'echo HISTORY_NEWER\r'); shell.until(b'LAB2_PROMPT> ')
            shell.send(b'\x12'); shell.until(b'reverse-i-search')
            shell.send(b'echo HISTORY_'); shell.until(b'HISTORY_NEWER')
            shell.send(b'\x12'); shell.until(b'HISTORY_OLD')
            shell.send(b'\x1b[C\x05_EDITED\r')
            result=shell.until(b'LAB2_PROMPT> ')
            if b'HISTORY_OLDER_EDITED' not in result:
                result += shell.until(b'LAB2_PROMPT> ')
            assert b'HISTORY_OLDER_EDITED' in result, repr(result)
            shell.send(b'\x12'); shell.until(b'reverse-i-search')
            shell.send(b'\x07'); shell.until(b'LAB2_PROMPT> ')
            shell.send(b'history | grep -F HISTORY_NEWER\r')
            assert b'echo HISTORY_NEWER' in shell.until(b'LAB2_PROMPT> ')
            print('Bash: history filtering, Ctrl+R, older match, edit-before-run, and Ctrl+G passed.')
        finally:
            shell.close()
        path=Path(folder)/'edit.txt'
        path.write_text('Room: Hall-0\n')
        editor=Session(['nano','--ignorercfiles',str(path)],folder)
        try:
            editor.until(b'Room: Hall-0')
            editor.send(b'\x05\x7f3\x0f')
            editor.until(b'File Name to')
            editor.send(b'\r'); editor.until(b'Wrote')
            editor.send(b'\x18')
            assert path.read_text()=='Room: Hall-3\n'
            print('nano: edit, Ctrl+O, filename confirmation, and saved bytes passed.')
        finally:
            editor.close()
        long=Path(folder)/'long.txt'
        original='\n'.join('NEEDLE_FIRST' if i==40 else 'NEEDLE_SECOND' if i==80 else f'Line {i}' for i in range(120))+'\n'
        long.write_text(original)
        pager=Session(['less',str(long)],folder)
        try:
            pager.until(b'Line 0')
            pager.send(b'/NEEDLE\r'); pager.until(b'FIRST')
            pager.send(b'n'); pager.until(b'SECOND')
            pager.send(b'N'); pager.until(b'FIRST')
            pager.send(b'q')
            assert long.read_text()==original
            print('less: search, next/previous match, quit, and unchanged source passed.')
        finally:
            pager.close()


if __name__=='__main__':
    main()
