from traces import instrumented_trace


@instrumented_trace()
def teste():
    print('teste')


teste()
