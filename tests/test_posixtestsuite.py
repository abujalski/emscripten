#!/usr/bin/env python
#
# coding=utf-8
# Copyright 2020 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

from __future__ import print_function
import os
import site

from runner import BrowserCore, path_from_root

# TODO: Fix failing tests
# TODO: Check if these tests runs with asm.js.
# TODO: Check if these tests works with node.js.


def requires_threads(f):
  def decorated(self, *args, **kwargs):
    if os.environ.get('EMTEST_LACKS_THREAD_SUPPORT'):
      self.skipTest('EMTEST_LACKS_THREAD_SUPPORT is set')
    return f(self, *args, **kwargs)

  return decorated


posix_tests_root_dir = path_from_root('tests', 'third_party', 'posixtestsuite')


def posix_testsuite_path(*pathelems):
  return os.path.join(posix_tests_root_dir, *pathelems)


posix_tests_common_args = [
  '-O3',
  '-Wno-format-security',
  '-Wno-macro-redefined',  # Some test define _XOPEN_SOURCE macro
  '-s', 'TOTAL_MEMORY=134217728',
  '-s', 'TOTAL_STACK=16777216',
  '-s', 'EXIT_RUNTIME=1',
  '-I', posix_testsuite_path('include'),
  '-include', path_from_root('tests', 'test_posixtestsuite_common.h'),
  '--pre-js', path_from_root('tests', 'test_posixtestsuite_prejs.js'),
]


def posix_test_dir(suite):
  return posix_testsuite_path('conformance', 'interfaces', suite)


def posix_test_file(suite, tc):
  return posix_testsuite_path('conformance', 'interfaces', suite, tc)


# Needed for python2, as it is missing partialmethod
def make_posix_test_case(func, suite, tc, requires_threads, thread_count=0):
  test_args = posix_tests_common_args + ['-I', posix_test_dir(suite)]
  if requires_threads:
    test_args = test_args + [
      '-s', 'USE_PTHREADS=1',
      '-s', 'PTHREAD_POOL_SIZE={}'.format(thread_count)]

  args = [posix_test_file(suite, tc + '.c')]
  keywords = {'expected': '0', 'args': test_args}

  def run_posix_test(self):
    return func(self, *args, **keywords)

  run_posix_test.func = func
  run_posix_test.args = args
  run_posix_test.keywords = keywords
  return run_posix_test


# List of all available POSIX test valid in browser environment,
# i.e. fork and signal tests are excluded
posix_test_cases = [
  ['asctime', '1-1', False],
  # Test fails: Error with processor times T1=0.00, T2=0.00
  # ['clock', '1-1', False],
  ['clock', '2-1', False],
  ['clock_getres', '1-1', False],
  ['clock_getres', '3-1', False],
  ['clock_getres', '5-1', False],
  ['clock_getres', '6-1', False],
  ['clock_getres', '6-2', False],
  ['clock_gettime', '1-1', False],
  ['clock_gettime', '1-2', False],
  ['clock_gettime', '2-1', False],
  ['clock_gettime', '3-1', False],
  ['clock_gettime', '7-1', False],
  ['clock_gettime', '8-1', False],
  ['clock_gettime', '8-2', False],
  ['ctime', '1-1', False],
  ['difftime', '1-1', False],
  ['fsync', '4-1', False],
  ['fsync', '5-1', False],
  # Test fails: fsync/7-1.c Test Fail: Expect EINVAL, get: No error information
  # ['fsync', '7-1', False],
  ['gmtime', '1-1', False],
  ['gmtime', '2-1', False],
  ['localtime', '1-1', False],
  ['mktime', '1-1', False],
  ['mmap', '1-1', False],
  ['mmap', '1-2', False],
  ['mmap', '5-1', False],
  ['mmap', '6-1', False],
  ['mmap', '6-2', False],
  ['mmap', '6-3', False],
  ['mmap', '6-4', False],
  ['mmap', '6-5', False],
  ['mmap', '6-6', False],
  ['mmap', '7-1', False],
  ['mmap', '7-2', False],
  ['mmap', '9-1', False],
  ['mmap', '10-1', False],
  ['mmap', '11-1', False],
  ['mmap', '12-1', False],
  ['mmap', '13-1', False],
  ['mmap', '14-1', False],
  ['mmap', '19-1', False],
  # Test failed by OOM: RuntimeError: abort(OOM). Build with -s ASSERTIONS=1 for more info.
  # ['mmap', '24-1', False],
  ['mmap', '24-2', False],
  ['munmap', '2-1', False],
  ['munmap', '4-1', False],
  ['munmap', '8-1', False],
  ['munmap', '9-1', False],
  # Test fail: nanosleep() did not sleep long enough
  # ['nanosleep', '1-1', False],
  # Test fail: "At least one test FAILED"
  # ['nanosleep', '2-1', False],
  ['nanosleep', '5-1', False],
  ['nanosleep', '6-1', False],
  ['nanosleep', '10000-1', False],
  ['pthread_attr_destroy', '1-1', True, 8],
  ['pthread_attr_destroy', '2-1', True, 8],
  ['pthread_attr_destroy', '3-1', True, 8],
  ['pthread_attr_getdetachstate', '1-1', True, 8],
  ['pthread_attr_getdetachstate', '1-2', True, 8],
  ['pthread_attr_getinheritsched', '1-1', True, 8],
  ['pthread_attr_getschedparam', '1-1', True, 8],
  ['pthread_attr_getschedpolicy', '2-1', True, 8],
  ['pthread_attr_getscope', '1-1', True, 8],
  ['pthread_attr_getstack', '1-1', True, 8],
  ['pthread_attr_getstacksize', '1-1', True, 8],
  ['pthread_attr_init', '1-1', True, 8],
  ['pthread_attr_init', '2-1', True, 8],
  ['pthread_attr_init', '3-1', True, 8],
  ['pthread_attr_init', '4-1', True, 8],
  ['pthread_attr_setdetachstate', '1-1', True, 8],
  ['pthread_attr_setdetachstate', '1-2', True, 8],
  ['pthread_attr_setdetachstate', '2-1', True, 8],
  ['pthread_attr_setdetachstate', '4-1', True, 8],
  ['pthread_attr_setinheritsched', '1-1', True, 8],
  ['pthread_attr_setinheritsched', '2-1', True, 8],
  ['pthread_attr_setinheritsched', '2-2', True, 8],
  ['pthread_attr_setinheritsched', '2-3', True, 8],
  ['pthread_attr_setinheritsched', '2-4', True, 8],
  ['pthread_attr_setinheritsched', '4-1', True, 8],
  ['pthread_attr_setschedparam', '1-1', True, 8],
  ['pthread_attr_setschedparam', '1-2', True, 8],
  ['pthread_attr_setschedparam', '1-3', True, 8],
  ['pthread_attr_setschedparam', '1-4', True, 8],
  ['pthread_attr_setschedpolicy', '1-1', True, 8],
  ['pthread_attr_setschedpolicy', '4-1', True, 8],
  ['pthread_attr_setscope', '1-1', True, 8],
  ['pthread_attr_setscope', '4-1', True, 8],
  ['pthread_attr_setstack', '1-1', True, 8],
  # Test fails to compile
  # ['pthread_attr_setstack', '2-1', True, 8],
  ['pthread_attr_setstack', '4-1', True, 8],
  ['pthread_attr_setstack', '7-1', True, 8],
  ['pthread_attr_setstacksize', '1-1', True, 8],
  # Test fails to compile
  # ['pthread_attr_setstacksize', '2-1', True, 8],
  ['pthread_barrier_destroy', '1-1', True, 8],
  ['pthread_barrier_destroy', '2-1', True, 8],
  ['pthread_barrier_init', '1-1', True, 8],
  ['pthread_barrier_init', '3-1', True, 8],
  ['pthread_barrier_init', '4-1', True, 8],
  ['pthread_barrier_wait', '1-1', True, 8],
  # This tests fails sometimes on FF was working well on Chrome.
  # ['pthread_barrier_wait', '2-1', True, 8],
  ['pthread_barrier_wait', '6-1', True, 8],
  ['pthread_barrierattr_destroy', '1-1', True, 8],
  ['pthread_barrierattr_getpshared', '1-1', True, 8],
  ['pthread_barrierattr_init', '1-1', True, 8],
  ['pthread_barrierattr_init', '2-1', True, 8],
  ['pthread_barrierattr_setpshared', '1-1', True, 8],
  ['pthread_barrierattr_setpshared', '2-1', True, 8],
  ['pthread_cancel', '1-1', True, 8],
  ['pthread_cancel', '1-2', True, 8],
  ['pthread_cancel', '1-3', True, 8],
  ['pthread_cancel', '2-1', True, 8],
  ['pthread_cancel', '2-2', True, 8],
  ['pthread_cancel', '2-3', True, 8],
  ['pthread_cancel', '3-1', True, 8],
  ['pthread_cancel', '4-1', True, 8],
  ['pthread_cancel', '5-1', True, 8],
  ['pthread_cleanup_pop', '1-1', True, 8],
  ['pthread_cleanup_pop', '1-2', True, 8],
  ['pthread_cleanup_pop', '1-3', True, 8],
  ['pthread_cleanup_push', '1-1', True, 8],
  ['pthread_cleanup_push', '1-2', True, 8],
  ['pthread_cleanup_push', '1-3', True, 8],
  ['pthread_cond_broadcast', '1-1', True, 8],
  ['pthread_cond_broadcast', '1-2', True, 102],
  ['pthread_cond_broadcast', '2-1', True, 8],
  ['pthread_cond_broadcast', '2-2', True, 8],
  ['pthread_cond_broadcast', '2-3', True, 21],
  ['pthread_cond_broadcast', '4-1', True, 8],
  ['pthread_cond_destroy', '1-1', True, 8],
  ['pthread_cond_destroy', '3-1', True, 8],
  ['pthread_cond_init', '1-1', True, 8],
  ['pthread_cond_init', '2-1', True, 8],
  ['pthread_cond_init', '3-1', True, 8],
  ['pthread_cond_signal', '1-2', True, 22],
  ['pthread_cond_signal', '2-1', True, 8],
  ['pthread_cond_signal', '2-2', True, 8],
  ['pthread_cond_signal', '4-1', True, 8],
  ['pthread_cond_timedwait', '1-1', True, 8],
  ['pthread_cond_timedwait', '2-1', True, 8],
  ['pthread_cond_timedwait', '2-2', True, 8],
  ['pthread_cond_timedwait', '2-3', True, 8],
  ['pthread_cond_timedwait', '2-5', True, 33],
  ['pthread_cond_timedwait', '2-6', True, 8],
  ['pthread_cond_timedwait', '3-1', True, 8],
  ['pthread_cond_timedwait', '4-1', True, 8],
  ['pthread_cond_timedwait', '4-2', True, 22],
  ['pthread_cond_wait', '1-1', True, 8],
  ['pthread_cond_wait', '2-1', True, 8],
  ['pthread_cond_wait', '2-3', True, 8],
  ['pthread_cond_wait', '3-1', True, 8],
  ['pthread_condattr_destroy', '1-1', True, 8],
  ['pthread_condattr_destroy', '2-1', True, 8],
  ['pthread_condattr_destroy', '3-1', True, 8],
  ['pthread_condattr_destroy', '4-1', True, 8],
  ['pthread_condattr_getclock', '1-1', True, 8],
  ['pthread_condattr_getclock', '1-2', True, 8],
  ['pthread_condattr_getpshared', '1-1', True, 8],
  ['pthread_condattr_getpshared', '1-2', True, 8],
  ['pthread_condattr_getpshared', '2-1', True, 8],
  ['pthread_condattr_init', '1-1', True, 8],
  ['pthread_condattr_init', '3-1', True, 8],
  ['pthread_condattr_setclock', '1-1', True, 8],
  ['pthread_condattr_setclock', '1-2', True, 8],
  ['pthread_condattr_setclock', '1-3', True, 8],
  ['pthread_condattr_setclock', '2-1', True, 8],
  ['pthread_condattr_setpshared', '1-1', True, 8],
  ['pthread_condattr_setpshared', '1-2', True, 8],
  ['pthread_condattr_setpshared', '2-1', True, 8],
  ['pthread_create', '1-1', True, 8],
  ['pthread_create', '1-2', True, 8],
  ['pthread_create', '1-3', True, 8], # Test depends on signals, may hangs on failure
  ['pthread_create', '1-4', True, 21],
  ['pthread_create', '1-6', True, 34],
  ['pthread_create', '2-1', True, 8],
  ['pthread_create', '3-1', True, 8],
  ['pthread_create', '3-2', True, 8],
  ['pthread_create', '4-1', True, 8],
  ['pthread_create', '5-1', True, 8],
  ['pthread_create', '5-2', True, 8],
  ['pthread_create', '12-1', True, 8],
  ['pthread_create', '15-1', True, 21],
  ['pthread_detach', '1-1', True, 8],
  ['pthread_detach', '1-2', True, 34],
  ['pthread_detach', '2-1', True, 8],
  ['pthread_detach', '2-2', True, 34],
  ['pthread_detach', '3-1', True, 8],
  ['pthread_detach', '4-1', True, 8],
  ['pthread_detach', '4-2', True, 8],
  ['pthread_equal', '1-1', True, 8],
  ['pthread_equal', '1-2', True, 8],
  ['pthread_exit', '1-1', True, 8],
  ['pthread_exit', '1-2', True, 8],
  ['pthread_exit', '2-1', True, 8],
  ['pthread_exit', '2-2', True, 8],
  ['pthread_exit', '3-1', True, 8],
  ['pthread_exit', '3-2', True, 8],
  # Tests hangs: "exception thrown: RuntimeError: function signature mismatch,RuntimeError: function signature mismatch"
  # POSIX spec requires that functions registered as exit handler to have prototype "void(void)" however Emscripten
  # calls them as Object.Module.dynCall_vi in callRuntimeCallbacks
  # ['pthread_exit', '4-1', True, 8],
  # Tests hangs: "exception thrown: RuntimeError: function signature mismatch,RuntimeError: function signature mismatch"
  # POSIX spec requires that functions registered as exit handler to have prototype "void(void)" however Emscripten
  # calls them as Object.Module.dynCall_vi in callRuntimeCallbacks
  # ['pthread_exit', '5-1', True, 8],
  ['pthread_exit', '6-2', True, 21],
  ['pthread_getcpuclockid', '1-1', True, 8],
  ['pthread_getschedparam', '1-1', True, 8],
  ['pthread_getschedparam', '1-2', True, 8],
  ['pthread_getschedparam', '1-3', True, 8],
  ['pthread_getspecific', '1-1', True, 8],
  ['pthread_getspecific', '3-1', True, 8],
  ['pthread_join', '1-1', True, 8],
  ['pthread_join', '1-2', True, 8],
  ['pthread_join', '2-1', True, 8],
  ['pthread_join', '3-1', True, 8],
  ['pthread_join', '4-1', True, 8],
  ['pthread_join', '5-1', True, 8],
  ['pthread_join', '6-2', True, 8],
  ['pthread_key_create', '1-1', True, 8],
  ['pthread_key_create', '1-2', True, 8],
  ['pthread_key_create', '2-1', True, 8],
  ['pthread_key_create', '3-1', True, 8],
  ['pthread_key_delete', '1-1', True, 8],
  ['pthread_key_delete', '1-2', True, 8],
  ['pthread_key_delete', '2-1', True, 8],
  ['pthread_mutex_destroy', '1-1', True, 8],
  ['pthread_mutex_destroy', '2-1', True, 8],
  ['pthread_mutex_destroy', '2-2', True, 8],
  ['pthread_mutex_destroy', '3-1', True, 8],
  ['pthread_mutex_destroy', '5-1', True, 8],
  ['pthread_mutex_destroy', '5-2', True, 8],
  ['pthread_mutex_init', '1-1', True, 8],
  ['pthread_mutex_init', '1-2', True, 8],
  ['pthread_mutex_init', '2-1', True, 8],
  ['pthread_mutex_init', '3-1', True, 8],
  ['pthread_mutex_init', '3-2', True, 8],
  ['pthread_mutex_init', '4-1', True, 8],
  ['pthread_mutex_lock', '1-1', True, 8],
  ['pthread_mutex_lock', '2-1', True, 8],
  ['pthread_mutex_lock', '4-1', True, 8],
  ['pthread_mutex_timedlock', '1-1', True, 8],
  ['pthread_mutex_timedlock', '2-1', True, 8],
  ['pthread_mutex_timedlock', '4-1', True, 8],
  ['pthread_mutex_timedlock', '5-1', True, 8],
  ['pthread_mutex_timedlock', '5-2', True, 8],
  ['pthread_mutex_timedlock', '5-3', True, 8],
  ['pthread_mutex_trylock', '1-1', True, 8],
  ['pthread_mutex_trylock', '3-1', True, 8],
  ['pthread_mutex_trylock', '4-1', True, 8],
  ['pthread_mutex_unlock', '1-1', True, 8],
  ['pthread_mutex_unlock', '2-1', True, 8],
  ['pthread_mutex_unlock', '3-1', True, 8],
  ['pthread_mutex_unlock', '5-1', True, 8],
  ['pthread_mutex_unlock', '5-2', True, 8],
  ['pthread_mutexattr_destroy', '1-1', True, 8],
  ['pthread_mutexattr_destroy', '2-1', True, 8],
  ['pthread_mutexattr_destroy', '3-1', True, 8],
  ['pthread_mutexattr_destroy', '4-1', True, 8],
  ['pthread_mutexattr_getpshared', '1-1', True, 8],
  ['pthread_mutexattr_getpshared', '1-2', True, 8],
  ['pthread_mutexattr_getpshared', '1-3', True, 8],
  ['pthread_mutexattr_getpshared', '3-1', True, 8],
  ['pthread_mutexattr_gettype', '1-1', True, 8],
  ['pthread_mutexattr_gettype', '1-2', True, 8],
  ['pthread_mutexattr_gettype', '1-3', True, 8],
  ['pthread_mutexattr_gettype', '1-4', True, 8],
  ['pthread_mutexattr_gettype', '1-5', True, 8],
  ['pthread_mutexattr_init', '1-1', True, 8],
  ['pthread_mutexattr_init', '3-1', True, 8],
  ['pthread_mutexattr_setpshared', '1-1', True, 8],
  ['pthread_mutexattr_setpshared', '1-2', True, 8],
  ['pthread_mutexattr_setpshared', '2-1', True, 8],
  ['pthread_mutexattr_setpshared', '2-2', True, 8],
  ['pthread_mutexattr_setpshared', '3-1', True, 8],
  ['pthread_mutexattr_setpshared', '3-2', True, 8],
  ['pthread_mutexattr_settype', '1-1', True, 8],
  ['pthread_mutexattr_settype', '3-1', True, 8],
  ['pthread_mutexattr_settype', '3-2', True, 8],
  ['pthread_mutexattr_settype', '3-3', True, 8],
  ['pthread_mutexattr_settype', '3-4', True, 8],
  ['pthread_mutexattr_settype', '7-1', True, 8],
  ['pthread_once', '1-1', True, 8],
  ['pthread_once', '1-2', True, 8],
  ['pthread_once', '1-3', True, 32],
  ['pthread_once', '2-1', True, 8],
  ['pthread_once', '3-1', True, 8],
  ['pthread_once', '4-1', True, 8],
  ['pthread_rwlock_destroy', '1-1', True, 8],
  ['pthread_rwlock_destroy', '3-1', True, 8],
  ['pthread_rwlock_init', '1-1', True, 8],
  ['pthread_rwlock_init', '2-1', True, 8],
  ['pthread_rwlock_init', '3-1', True, 8],
  ['pthread_rwlock_init', '6-1', True, 8],
  ['pthread_rwlock_rdlock', '1-1', True, 8],
  ['pthread_rwlock_rdlock', '2-3', True, 8],
  ['pthread_rwlock_rdlock', '5-1', True, 8],
  ['pthread_rwlock_timedrdlock', '1-1', True, 8],
  ['pthread_rwlock_timedrdlock', '2-1', True, 8],
  ['pthread_rwlock_timedrdlock', '3-1', True, 8],
  ['pthread_rwlock_timedrdlock', '5-1', True, 8],
  ['pthread_rwlock_timedwrlock', '1-1', True, 8],
  ['pthread_rwlock_timedwrlock', '2-1', True, 8],
  ['pthread_rwlock_timedwrlock', '3-1', True, 8],
  ['pthread_rwlock_timedwrlock', '5-1', True, 8],
  ['pthread_rwlock_tryrdlock', '1-1', True, 8],
  ['pthread_rwlock_trywrlock', '1-1', True, 8],
  ['pthread_rwlock_unlock', '1-1', True, 8],
  ['pthread_rwlock_unlock', '2-1', True, 8],
  ['pthread_rwlock_unlock', '4-1', True, 8],
  ['pthread_rwlock_unlock', '4-2', True, 8],
  ['pthread_rwlock_wrlock', '1-1', True, 8],
  ['pthread_rwlock_wrlock', '3-1', True, 8],
  ['pthread_rwlockattr_destroy', '1-1', True, 8],
  ['pthread_rwlockattr_destroy', '2-1', True, 8],
  ['pthread_rwlockattr_getpshared', '1-1', True, 8],
  ['pthread_rwlockattr_getpshared', '4-1', True, 8],
  ['pthread_rwlockattr_init', '1-1', True, 8],
  ['pthread_rwlockattr_init', '2-1', True, 8],
  ['pthread_rwlockattr_setpshared', '1-1', True, 8],
  ['pthread_self', '1-1', True, 8],
  ['pthread_setcancelstate', '1-1', True, 8],
  ['pthread_setcancelstate', '1-2', True, 8],
  ['pthread_setcancelstate', '2-1', True, 8],
  ['pthread_setcancelstate', '3-1', True, 8],
  # Test fails due to musl bug.
  # ['pthread_setcanceltype', '1-1', True, 8],
  ['pthread_setcanceltype', '1-2', True, 8],
  ['pthread_setcanceltype', '2-1', True, 8],
  ['pthread_setschedparam', '1-1', True, 8],
  ['pthread_setschedparam', '1-2', True, 8],
  ['pthread_setschedparam', '4-1', True, 8],
  ['pthread_setschedprio', '1-1', True, 8],
  ['pthread_setspecific', '1-1', True, 8],
  ['pthread_setspecific', '1-2', True, 8],
  ['pthread_spin_destroy', '1-1', True, 8],
  ['pthread_spin_destroy', '3-1', True, 8],
  ['pthread_spin_init', '1-1', True, 8],
  ['pthread_spin_init', '4-1', True, 8],
  ['pthread_spin_lock', '1-2', True, 8],
  ['pthread_spin_lock', '3-2', True, 8],
  ['pthread_spin_trylock', '1-1', True, 8],
  ['pthread_spin_trylock', '4-1', True, 8],
  ['pthread_spin_unlock', '1-1', True, 8],
  ['pthread_spin_unlock', '1-2', True, 8],
  ['pthread_spin_unlock', '3-1', True, 8],
  ['pthread_testcancel', '1-1', True, 8],
  ['pthread_testcancel', '2-1', True, 8],
  ['strftime', '1-1', False],
  ['strftime', '2-1', False],
  ['strftime', '3-1', False],
  ['time', '1-1', False],
]


class posixtestsuite(BrowserCore):
  """ Class defines methods for running test cases from Open POSIX test suite fork.
      This class runs only tests which are valid tests to run in the browser environment
      i.e. excluded test includes ones checking forking, signals."""

  @classmethod
  def setUpClass(cls):
    super(posixtestsuite, cls).setUpClass()
    cls.browser_timeout = 90
    if not os.path.isdir(posix_tests_root_dir):
      raise IOError('Open POSIX tests suite not cloned. Please run \'git submodule update --init\'')

    print()
    print('Running the Open POSIX tests in the browser. Make sure the browser allows popups from localhost.')
    print()

  @classmethod
  def add_test_cases(cls):
    for t in posix_test_cases:
      tc_name = 'test_' + t[0] + '_' + t[1].replace('-', '_')
      requires_threads = t[2]
      thread_count = 0
      if requires_threads:
        thread_count = t[3]

      setattr(cls,
              tc_name,
              make_posix_test_case(cls.btest,
                                   t[0],
                                   t[1],
                                   requires_threads,
                                   thread_count))


posixtestsuite.add_test_cases()
