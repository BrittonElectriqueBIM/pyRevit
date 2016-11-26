""" Module name: compiler.py
Copyright (c) 2014-2016 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE


~~~
Description:

"""
import os.path as op

from ..config import ASSEMBLY_FILE_TYPE
from ..exceptions import PyRevitException

from System import Array
from System.CodeDom import Compiler
from Microsoft.CSharp import CSharpCodeProvider


def compile_to_asm(code, name, output_dir, references=None):

    compiler_params = Compiler.CompilerParameters()
    compiler_params.OutputAssembly = op.join(output_dir, name + ASSEMBLY_FILE_TYPE)

    compiler_params.TreatWarningsAsErrors = False
    compiler_params.GenerateExecutable = False
    compiler_params.CompilerOptions = "/optimize"

    for reference in references or []:
        compiler_params.ReferencedAssemblies.Add(reference)

    provider = CSharpCodeProvider()
    compiler = provider.CompileAssemblyFromSource(compiler_params, Array[str]([code]))

    if compiler.Errors.HasErrors:
        error_list = [str(err) for err in compiler.Errors.GetEnumerator()]
        raise PyRevitException("Compile error: {}".format(error_list))

    return compiler.PathToAssembly
