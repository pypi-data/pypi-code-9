def validate_args(args):

    mergecol, intype, outtype = args["mergecol"], args["intype"], args["outtype"]

    if not len(mergecol) == len(intype) == len(outtype):

        msg = "Number of args for --column, --intype and --outtype must be equal," \
              " but they are not: --column {} {} \n--intype {} {} \n--outtype {} {}" \
                  .format(mergecol, len(mergecol), intype, len(intype), \
                          outtype, len(outtype))
        raise ValueError(msg)
