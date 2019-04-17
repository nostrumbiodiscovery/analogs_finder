import os

def sdf_to_mae(sdf, output=None):
    if not output:
        output = os.path.splitext(os.path.basename(sdf))[0]+".mae"
    sdconvert = os.path.join(os.environ["SCHRODINGER"], "utilities/sdconvert")
    command = "{} -isdf {}  -omae {} > /dev/null".format(sdconvert, sdf, output)
    print(command)
    os.system(command)
    return output
