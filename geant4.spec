### RPM external geant4 10.00.p01

%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source0: http://geant4.cern.ch/support/source/%{n}.%{realversion}.tar.gz

%if "%mic" != "true"
BuildRequires: cmake
%endif

Requires: clhep
Requires: expat
Requires: xerces-c

%define keep_archives true

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%prep
%setup -n %{n}.%{realversion}

%build

SOEXT=so
if [ $(uname) = Darwin ]; then
  SOEXT=dylib
fi

rm -rf ../build
mkdir ../build
cd ../build

%if "%mic" == "true"
cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="icpc" \
  -DCMAKE_CXX_FLAGS="-mmic" \
  -DCMAKE_C_COMPILER="icc" \
  -DCMAKE_C_FLAGS="-mmic" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_BUILD_MULTITHREADED=OFF \
%else
cmake ../%{n}.%{realversion} \
  -DCMAKE_CXX_COMPILER="%cms_cxx" \
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_INSTALL_LIBDIR="lib" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGEANT4_USE_GDML=ON \
  -DGEANT4_BUILD_CXXSTD:STRING="c++11" \
  -DGEANT4_ENABLE_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DXERCESC_ROOT_DIR:PATH="${XERCES_C_ROOT}" \
  -DCLHEP_ROOT_DIR:PATH="$CLHEP_ROOT" \
  -DEXPAT_INCLUDE_DIR:PATH="$EXPAT_ROOT/include" \
  -DEXPAT_LIBRARY:FILEPATH="$EXPAT_ROOT/lib/libexpat.$SOEXT" \
  -DBUILD_STATIC_LIBS=ON \
  -DGEANT4_INSTALL_EXAMPLES=OFF \
  -DGEANT4_USE_SYSTEM_CLHEP=ON \
  -DGEANT4_BUILD_MULTITHREADED=OFF \
%endif

make %makeprocesses

%install

cd ../build
make install

mkdir -p %i/lib/archive
cd %i/lib/archive
find %i/lib -name "*.a" -exec ar x {} \;
ar rcs libgeant4-static.a *.o
find . -name "*.o" -delete

%post
%{relocateConfig}lib/Geant4-*/Geant4Config.cmake
