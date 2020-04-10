class SoftAssert:
    """
    class used to mimic the soft asserts.

    """

    def __init__(self):
        # asserts property will contain a list of asserts that have occur during the test flow
        self.asserts = []

    def assert_all(self):
        """Asserts all the failed items under the self.asserts list

        This method should be called at the end of the test,
        to raise the failures that were found during the test flow

        :return: None
        """
        failed_asserts = list(filter(lambda a: not a.get('result'), self.asserts))
        err_msgs = []

        for failed_assert in failed_asserts:
            err_msgs.append(f"\t\"{failed_assert.get('actual')}\" "
                            f"{failed_assert.get('conditional')} "
                            f"\"{failed_assert.get('expected')}\", "
                            f"\"{failed_assert.get('message')}\"\n"
                            f"\t\tStatus result: FAILED ")

        # reset asserts
        self.asserts = []

        if len(failed_asserts):
            print("ERROR: Below failures were found during the test execution")
            str_err_msgs = "\n".join(err_msgs)
            print(str_err_msgs)
            raise AssertionError(str_err_msgs)

    def verify(self, actual, expected, message: str, assert_all: bool = False) -> bool:
        """Simple verify

        Verifies that :param actual matches with :param expected without stopping the test execution,
        this allows to assert multiple times on the same flow.

        :param actual: Actual value, normally obtained from the tested app
        :param expected: The expected value that should be on the tested app
        :param message:str: Assert message, used for reporting purposes
        :param assert_all: bool [optional], default: False,  if True and the conditional_result is False,
            the self.assert_all() method will be called
        :return: condition_result: bool
        """

        condition_result = actual == expected
        _assert = {
            "actual": actual,
            "expected": expected,
            "message": message,
            "conditional": "==",
            "result": condition_result,
        }
        print(f"\n{message}. Status: {'PASSED' if condition_result else 'FAILED'}")
        self.asserts.append(_assert)
        if assert_all:
            self.assert_all()

        return condition_result

    # TODO:
    def verify_contains(self, actual, in_expected_list, ):
        raise NotImplementedError

    # TODO:
    def verify_regex(self, actual, regex, ):
        raise NotImplementedError
