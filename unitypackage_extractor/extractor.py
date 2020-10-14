import tarfile
import tempfile
import os
import time
import shutil
import argparse


def extractPackage(packagePath, outputPath="", extractMetaFiles=True):
    """
    Extracts a .unitypackage into the current directory
    @param {string} packagePath The path to the .unitypackage
    @param {string} [outputPath=""] Optional output path, otherwise will use cwd
    @param {bool} [extractMetaFiles=True] Optional control over metafile extration
    """
    with tempfile.TemporaryDirectory() as tmpDir:
        # Unpack the whole thing in one go (faster than traversing the tar)
        with tarfile.open(name=packagePath) as upkg:
            upkg.extractall(tmpDir)

        # Extract each file in tmpDir to final destination
        for dirEntry in os.scandir(tmpDir):
            assetEntryDir = f"{tmpDir}/{dirEntry.name}"

            # we need a hint where to drop the asset file
            if not os.path.exists(f"{assetEntryDir}/pathname"):
                continue

            # Has the required info to extract
            # Get the path to output to from /pathname
            with open(f"{assetEntryDir}/pathname") as f:
                pathname, assetname = os.path.split(f.readline().rstrip('\n'))

            # Are we dealing with just a folder?
            if not os.path.exists(f"{assetEntryDir}/asset"):
                print(f"Extracting '{dirEntry.name}' as Folder to '{pathname}/{assetname}'")
                os.makedirs(os.path.join(
                    outputPath, pathname, assetname), exist_ok=True)

                if extractMetaFiles:
                    print(f"Extracting '{dirEntry.name}' as Folder Meta to '{pathname}/{assetname}'.meta")
                    metaSourcePath = f"{assetEntryDir}/asset.meta"
                    metaTargetPath = os.path.join(
                        outputPath, pathname, f"{assetname}.meta")
                    if os.path.exists(metaSourcePath):
                        shutil.move(metaSourcePath, metaTargetPath)
            else:  # Its actualy a asset!
                print(f"Extracting '{dirEntry.name}' as Asset to '{pathname}/{assetname}'")
                os.makedirs(os.path.join(outputPath, pathname), exist_ok=True)

                assetSourcePath = f"{assetEntryDir}/asset"
                assetTargetPath = os.path.join(outputPath, pathname, assetname)
                shutil.move(assetSourcePath, assetTargetPath)

                if extractMetaFiles:
                    print(f"Extracting '{dirEntry.name}' as Asset Meta to '{pathname}/{assetname}.meta'")
                    metaSourcePath = f"{assetEntryDir}/asset.meta"
                    metaTargetPath = os.path.join(
                        outputPath, pathname, f"{assetname}.meta")
                    if os.path.exists(metaSourcePath):
                        shutil.move(metaSourcePath, metaTargetPath)


def _get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('input',
                        help='Path to *.unitypackage file')

    parser.add_argument('-o', '--output',
                        help='Writes the contents to the given folder',
                        default="",
                        metavar='<output>')

    parser.add_argument('-nm', '--nometa',
                        help='Don\'t extract meta files',
                        action='store_true')

    return parser


def _process_parser_result(args):
    startTime = time.time()
    extractPackage(args.input, args.output, not args.nometa)
    print("--- Finished in %s seconds ---" % (time.time() - startTime))


def cli(args=None):
    parser = _get_parser()
    _process_parser_result(parser.parse_args(args))


if __name__ == "__main__":
    cli()
