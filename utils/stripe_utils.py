import stripe
from django.conf import settings



def handleStripeError(f):
        def handleProblems(*args, **kwargs):
            response = {
                'paid': False,
                'response_object': None,
                'error': None
            }
            common_message = "Currently its not possible to make payments."

            try:
                response_object = f(*args, **kwargs)
                response  = {
                    'response_object': response_object,
                    'error': None
                }
                return response
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body['error']
                response.update({'error':err['message']})
                return response
            except stripe.error.RateLimitError as e:
                response.update({'error':"Too many requests made to the API too quickly"})
                return response
            except stripe.error.InvalidRequestError as e:
                response.update({'error':"Invalid parameters"})
                return response
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                response.update({'error':common_message})
                return response
            except stripe.error.APIConnectionError as e:
                response.update({'error':common_message})
                return response
            except stripe.error.StripeError as e:
                # maybe send email
                response.update({'error':common_message})
                return response
            except Exception as e:
                # maybe send email
                response.update({'error':common_message})
                return response
        return handleProblems


class StripeUtils(object):

    CURRENCY = 'chf'
    INTERVAL = 'month'
    SUCCEEDED_STATUS = 'succeeded'

    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_API_PRIVATE_KEY

    @handleStripeError
    def create_customer(self, token, email):
        customer = self.stripe.Customer.create(
              source=token,
              description='description for testing',
              email=email
        )
        return customer

    @handleStripeError
    def make_charge(self, amount=None, customer=None):
        amount = int(amount * 100)  # stripe amount unit, in cents
        charge = self.stripe.Charge.create(
          amount=amount,  # in cents
          currency=self.CURRENCY,
          customer=customer
        )
        return charge

    @handleStripeError
    def create_plan(self, amount, name, id):
        self.stripe.Plan.create(
          amount=amount,
          interval=self.INTERVAL,
          name=name,
          currency=self.CURRENCY,
          id=id)

    def make_payment(self, user, amount, token):
        try:
            # Use Stripe's library to make requests...
            charge = self.stripe.Charge.create(
                amount=amount,
                currency=self.CURRENCY,
                source=token,
                description=settings.STRIPE_DESCRIPTION_ON_PAYMENT
            )

            if charge.get('status') == self.SUCCEEDED_STATUS:
                # do something
                pass
            return charge['status']
        except self.stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            return err['message']
        except self.stripe.error.RateLimitError as e:
            return "Too many requests made to the API too quickly"
        except self.stripe.error.InvalidRequestError as e:
            return "Invalid parameters"
        except self.stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except self.stripe.error.APIConnectionError as e:
            return "Currently its not possible to make payments."
        except self.stripe.error.StripeError as e:
            # maybe send email
            return "Currently its not possible to make payments."
        except Exception as e:
            # maybe send email
            return "Currently its not possible to make payments."