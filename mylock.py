from threading import Lock


class SafeLock:
    def __init__(self, timeout=10, attempts=3):
        """
        Creates a lock that automatically uses the provided timeout and will
        retry failed attempts a number of times equal to attempts. Each retry
        will increase the timeout exponentially.
        :param timeout: the timeout in milliseconds
        :param attempts:
        """
        self.lock = Lock()
        self.timeout = timeout
        self.maxattempts = attempts

    def acquire(self, blocking=True):
        return self._acquire(blocking, self.maxattempts)

    def _acquire(self, blocking, attempts):
        if attempts == 0:
            return False
        if self.lock.acquire(blocking, self._calc_timeout(attempts)):
            return True
        else:
            return self._acquire(blocking, attempts-1)

    def _calc_timeout(self, attempts_left):
        attemptnum = self.maxattempts - attempts_left + 1
        return (self.timeout ** attemptnum) / 1000

    def release(self):
        return self.lock.release()

    def locked(self):
        return self.lock.locked()

    def __enter__(self):
        if not self.acquire():
            raise FailedLockAcquisition()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class FailedLockAcquisition:
    pass


class MultiLock:
    def __init__(self, *locks):
        self.locks = locks

    def __enter__(self):
        for i, lock in enumerate(self.locks):
            if not lock.acquire():
                self.release_locks(i-1)
                raise FailedLockAcquisition()

    def release_locks(self, upto):
        if upto == 0:
            return
        for i, lock in enumerate(self.locks):
            if i > upto:
                return
            lock.release()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == FailedLockAcquisition:
            return  # if it was a FailedLockAcquisition, they've already been released
        for lock in self.locks:
            lock.release()
