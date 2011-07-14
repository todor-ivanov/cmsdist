### RPM external hepmc 2.05.01
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz
Patch0: hepmc-2.03.06-reflex

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n HepMC-%{realversion}
%patch0 -p0
case %cmsplatf in
  slc5_*_gcc4[01234]*) 
    F77="`which gfortran`"
    CXX="`which c++`"
    PLATF_CONFIG_OPTS=""
  ;;
  *)
    F77="`which gfortran` -fPIC"
    CXX="`which c++` -fPIC"
    PLATF_CONFIG_OPTS="--enable-static --disable-shared"
  ;;
esac
./configure $PLATF_CONFIG_OPTS --prefix=%{i} --with-momentum=GEV --with-length=MM F77="$F77" CXX="$CXX"

%build
make %makeprocesses

%install
make install
