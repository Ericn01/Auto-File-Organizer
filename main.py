'''
Main script
'''
import parser_builder
import configuration
import run_handling


def main():
    arg_config = configuration.load_arg_config()
    parser = parser_builder.build_parser(arg_config)
    args = parser.parse_args()

    if args.command == "config":
        run_handling.handle_config(args, arg_config)
    elif args.command == "run":
        run_handling.handle_run(args)


if __name__ == "__main__":
    main()
