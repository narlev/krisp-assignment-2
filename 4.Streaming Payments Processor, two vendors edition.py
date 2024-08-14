import io


def stream_payments(callback_fn):
    """
    Reads payments from a payment processor and calls `callback_fn(amount)`
    for each payment.
    Returns when there is no more payments.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in range(10):
        callback_fn(i)

# This is a library function, you can't modify it.
def store_payments(amount_iterator):
    """
    Iterates over the payment amounts from amount_iterator
    and stores them to a remote system.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in amount_iterator:
        print(i)


def process_payments_2():
    """
    Modify `process_payments_2()`, write glue code that enables
    `store_payments()` to consume payments produced by `stream_payments()`
    """

    # A generator function to act as an iterator for payments
    def payment_iterator():
        payments = []

        def callback_fn(amount):
            payments.append(amount)
        stream_payments(callback_fn)
        for payment in payments:
            yield payment

    # Using the generator to store payments
    store_payments(payment_iterator())


process_payments_2()
