import os
import zipfile

LOCAL_FOLDER = '/tmp'

# TODO: import shutil is probably simpler with shorter code to do the same operation
class Zip:
    """
    This class handles zipping files in dir.

    @note: consider removing the files once done.
    """
    def zipdir(path):
        """
        MISSING DOCSTRING.
        """
        # TOOD: @oran - we can move this elsewhere and give the user a choice
        #       where to dump the files
        os.makedirs(LOCAL_FOLDER, exist_ok=True)
        zipped_name = f'{filename}.zip'
        zipf = zipfile.ZipFile(zipped_name, 'w', zipfile.ZIP_DEFLATED)
        self._zipdir(LOCAL_FOLDER, zipf)
        zipf.close()

        return os.path.join(LOCAL_FOLDER, zipped_name)

    def _zipdir(path, ziph):
        """
        Helper method for zipdir.

        @type path: str
        @param path: path to dir
        @type ziph: zipfile.ZipFile
        @param ziph: zip file descriptor
        """
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
