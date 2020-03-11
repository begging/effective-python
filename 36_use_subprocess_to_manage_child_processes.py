import os
import subprocess
import time

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE)

out, err = proc.communicate()
print(out.decode('utf-8'))
print()

print('start sleep')
proc = subprocess.Popen(['sleep', '0.01'])
while proc.poll() is None:
    print('Working')
    # time.sleep(0.1)

print('Exit status', proc.poll())
print()

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time.time()
procs = []
for _ in range(10):
    proc = run_sleep(0.01)
    procs.append(proc)

for proc in procs:
    proc.communicate()

end = time.time()
print('Finished in %.3f seconds' % (end - start))
print()


def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() # Ensure the child gets input
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])


def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)

    return proc


input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

for proc in input_procs:
    proc.communicate()
for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())
print()

proc = run_sleep(10)
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
print()
