### RPM cms cmssw CMSSW_6_0_0_SLHCtkpre1
Requires: cmssw-tool-conf python

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

# Build with clang if _CLANG_X is in the name of the package.
%if "%(case %realversion in (*_CLANG_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_CLANG_X|_X|')
%define buildtarget     checker
%endif

%if "%(case %realversion in (*_EXPERIMENTAL_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_EXPERIMENTAL_X|_X|')
%define usercxxflags    -Ofast -march=native
%endif

%if "%(case %realversion in (*_COVERAGE_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_COVERAGE_X|_X|')
%define usercxxflags    -fprofile-arcs -ftest-coverage
%endif

%if "%(case %realversion in (*_FORTIFIED_X*) echo true ;; (*) echo false ;; esac)" == "true"
%define cvstag		%(echo %realversion | sed -e 's|_FORTIFIED_X|_X|')
%define usercxxflags    -fexceptions -fstack-protector-all --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2
%endif

## IMPORT scram-project-build
