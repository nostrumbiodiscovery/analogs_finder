import os
from analogs_finder.constants import constants as cs

def sdf_to_mae(sdf, schr=cs.SCHR, output=None):
    if not output:
        output = os.path.splitext(os.path.basename(sdf))[0]+".mae"
    sdconvert = os.path.join(schr, "utilities/sdconvert")
    command = "{} -isdf {}  -omae {} > /dev/null".format(sdconvert, sdf, output)
    print(command)
    os.system(command)
    return output
