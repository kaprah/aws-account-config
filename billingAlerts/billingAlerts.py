import boto3
import logging

# ================= LOGGING SETUP ================= #
logger = logging.getLogger('Billing_Alerts')
logging.basicConfig(format="({filename}:{lineno}) : {message}", style="{")
logging.getLogger("botocore").setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)

# ================= AWS SETUP ================= #
budgetClient = boto3.client("budgets")
stsClient = boto3.client("sts")
accountId = stsClient.get_caller_identity()["Account"]

# ================= OTHER VARIABLES ================= #
personalEmail = ""

def create_percentage_budget(client, accountId):
    logger.info("Creating ")
    response = client.create_budget(
        AccountId= accountId,
        Budget={
            'BudgetName': 'AWS fifty percent budget notification',
            'BudgetLimit': {
                'Amount': '25',
                'Unit': 'dollars'
            },
            'TimeUnit': 'MONTHLY',
            'CalculatedSpend': {
                'ActualSpend': {
                    'Amount': '25',
                    'Unit': 'dollars'
                },
                'ForecastedSpend': {
                    'Amount': '25',
                    'Unit': 'dollars'
                }
            },
            'BudgetType': 'USAGE',
        },
        NotificationsWithSubscribers=[
            {
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': 50,
                    'ThresholdType': 'PERCENTAGE',
                    'NotificationState': 'ALARM'
                },
                'Subscribers': [
                    {
                        'SubscriptionType': 'EMAIL',
                        'Address': personalEmail
                    },
                ]
            },
        ]
    )
    return response


budgetResponse = create_percentage_budget(budgetClient, accountId)
logger.info(f'Budget response: {budgetResponse}')