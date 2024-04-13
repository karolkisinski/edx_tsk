import logging
from handlers.mode_factory import HandlerFactory
from views.cli import parse_arguments

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    args = parse_arguments()

    try:
        handler = HandlerFactory.create_handler(args.mode)
        handler.process(currency=args.currency, amount=args.amount)
        logger.info("Job done!")
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
    main()
