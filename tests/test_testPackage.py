'''
Tests for package extracting
'''
import os
import unittest
import tempfile

from unitypackage_extractor.extractor import extractPackage

class TestTestPackageExtract(unittest.TestCase):
    '''
    Tests the package extracting functionality
    '''
    def test_packageExtract(self):
        '''should be able to extract a simple unity pckage'''
        #arrange
        with tempfile.TemporaryDirectory() as tmp:
            #test.unitypackage - Should contain one file named test.txt with the contents "testing"

            #act
            print(f"Extracting to {tmp}...")
            extractPackage("./tests/test.unitypackage", outputPath=tmp)

            #assert
            self.assertTrue(os.path.isdir(tmp))
            self.assertTrue(os.path.isdir(f"{tmp}/Assets"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt.meta"))
            self.assertEqual(open(f"{tmp}/Assets/test.txt").read(), "testing")

    def test_packageExtractWithoutMeta(self):
        '''should be able to extract a simple unity pckage'''
        #arrange
        with tempfile.TemporaryDirectory() as tmp:
            #test.unitypackage - Should contain one file named test.txt with the contents "testing"

            #act
            print(f"Extracting to {tmp}...")
            extractPackage("./tests/test.unitypackage", outputPath=tmp, extractMetaFiles=False)

            #assert
            self.assertTrue(os.path.isdir(tmp))
            self.assertTrue(os.path.isdir(f"{tmp}/Assets"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt"))
            self.assertFalse(os.path.exists(f"{tmp}/Assets/test.txt.meta"))
            self.assertEqual(open(f"{tmp}/Assets/test.txt").read(), "testing")

    def test_packageExtractWithLeadingDots(self):
        '''should be able to extract a unity package that contains ./ in every path in the tar'''
        #arrange
        with tempfile.TemporaryDirectory() as tmp:
            #testLeadingDots.unitypackage - Same as test.unitypackage but archived with `tar -zrf archive.unitypackage .`
            #to get the specific `./` before every path

            #act
            print(f"Extracting to {tmp}...")
            extractPackage("./tests/testLeadingDots.unitypackage", outputPath=tmp)

            #assert
            self.assertTrue(os.path.isdir(tmp))
            self.assertTrue(os.path.isdir(f"{tmp}/Assets"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt.meta"))
            self.assertEqual(open(f"{tmp}/Assets/test.txt").read(), "testing")

    def test_packageExtractWithLeadingDotsWithoutMeta(self):
        '''should be able to extract a unity package that contains ./ in every path in the tar'''
        #arrange
        with tempfile.TemporaryDirectory() as tmp:
            #testLeadingDots.unitypackage - Same as test.unitypackage but archived with `tar -zrf archive.unitypackage .`
            #to get the specific `./` before every path

            #act
            print(f"Extracting to {tmp}...")
            extractPackage("./tests/testLeadingDots.unitypackage", outputPath=tmp, extractMetaFiles=False)

            #assert
            self.assertTrue(os.path.isdir(tmp))
            self.assertTrue(os.path.isdir(f"{tmp}/Assets"))
            self.assertTrue(os.path.isfile(f"{tmp}/Assets/test.txt"))
            self.assertFalse(os.path.exists(f"{tmp}/Assets/test.txt.meta"))
            self.assertEqual(open(f"{tmp}/Assets/test.txt").read(), "testing")            