#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import step

#==============================================================================
# JobFactory Interface
#==============================================================================

class JobFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def job(self):
        pass

#==============================================================================
# JobFactory Interface
#==============================================================================

class InstallGoJobFactory(JobFactory):
    def job(self):
        job = step.Job('InstallGoJob')
        job.add(step.PathPrinter())
        job.add(step.GoDirectoryCleaner())
        job.add(step.GoDirectoryMaker())
        job.add(step.GoPackageDownloader())
        # job.add(step.GoPackageDecompressor())
        # job.add(step.GoPathDirectoryMaker())
        # job.add(step.GoEnvVariableModifier)
        return job

class InstallJavaJobFactory(JobFactory):
    def job(self):
        job = step.Job('InstallGoJob')
        job.add(step.PathPrinter())
        job.add(step.JavaDirectoryCleaner())
        job.add(step.JavaDirectoryMaker())
        job.add(step.JavaPackageDownloader())
        job.add(step.JavaPackageDecompressor())
        job.add(step.JavaEnvVariableModifier)
        return job

class InstallAllSoftwareJobFactory(JobFactory):
    def job(self):
        job = step.Job('InstallAllSoftwareJob')
        job.add(step.PathPrinter())
        job.add(step.AllDirectoryCleaner())
        job.add(InstallGoJobFactory().job())
        job.add(InstallJavaJobFactory().job())
        return job
