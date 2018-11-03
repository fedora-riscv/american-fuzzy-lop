# We need to rebuild this package every time the clang major version
# changes, since clang releases are not ABI compatible between major
# versions.  See also https://bugzilla.redhat.com/1544964
%global clang_major 6

Name:          american-fuzzy-lop
Version:       2.52b
Release:       6%{?dist}

Summary:       Practical, instrumentation-driven fuzzer for binary formats

License:       ASL 2.0

URL:           http://lcamtuf.coredump.cx/afl/
Source0:       http://lcamtuf.coredump.cx/afl/releases/afl-%{version}.tgz

# For running the tests:
Source1:       hello.c

# Upstream includes armv7hl support as some non-integrated 'contrib'
# files, so I have not enabled it here.  No other arch is supported
# without arch-specific changes.
ExclusiveArch: %{ix86} x86_64

BuildRequires: clang(major) = %{clang_major}
BuildRequires: llvm-devel

Requires:      gcc

%global afl_helper_path %{_libdir}/afl


%description
American fuzzy lop uses a novel type of compile-time instrumentation
and genetic algorithms to automatically discover clean, interesting
test cases that trigger new internal states in the targeted
binary. This substantially improves the functional coverage for the
fuzzed code. The compact synthesized corpuses produced by the tool are
also useful for seeding other, more labor- or resource-intensive
testing regimes down the road.

Compared to other instrumented fuzzers, afl-fuzz is designed to be
practical: it has a modest performance overhead, uses a variety of
highly effective fuzzing strategies, requires essentially no
configuration, and seamlessly handles complex, real-world use cases -
say, common image parsing or file compression libraries.


%package clang
Summary:       Clang and clang++ support for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      clang(major) = %{clang_major}


%description clang
This subpackage contains clang and clang++ support for
%{name}.


%package clang-fast
Summary:       Fast clang and clang++ support for %{name}
Requires:      %{name} = %{version}-%{release}
Requires:      clang(major) = %{clang_major}


%description clang-fast
This subpackage contains fast clang and clang++ support for
%{name}.

The code in this package allows you to instrument programs for AFL using
true compiler-level instrumentation, instead of the more crude
assembly-level rewriting approach taken by afl-gcc and afl-clang.


%prep
%setup -q -n afl-%{version}


%build

CFLAGS="%{optflags}" \
%{__make} %{?_smp_mflags} \
  PREFIX="%{_prefix}" \
  HELPER_PATH="%{afl_helper_path}" \
  DOC_PATH="%{_pkgdocdir}" \
  MISC_PATH="%{_pkgdocdir}"

# Build afl-clang-fast.
pushd llvm_mode

# Build llvm-config wrapper around the right binary for this arch.
%if 0%{?__isa_bits} == 32
%global llvm_config %{_bindir}/llvm-config-32
%else
%global llvm_config %{_bindir}/llvm-config-64
%endif
rm -f llvm-config
cat > llvm-config <<'EOF'
#!/bin/sh
%{llvm_config} "$@" | sed -e 's/-mcet//g' -e 's/-fcf-protection//g'
EOF
chmod 0755 llvm-config
cat ./llvm-config
./llvm-config --cflags
./llvm-config --cxxflags
./llvm-config --ldflags

# RPM flags include -mcet -fcf-protection which clang does not
# understand, so we have to remove them for now. XXX
fixed_cflags="$(echo %{optflags} |
                     sed -e 's/-mcet//g' -e 's/-fcf-protection//g')"
CFLAGS="$fixed_cflags" \
%{__make} %{?_smp_mflags} \
  PREFIX="%{_prefix}" \
  HELPER_PATH="%{afl_helper_path}" \
  DOC_PATH="%{_pkgdocdir}" \
  MISC_PATH="%{_pkgdocdir}" \
  LLVM_CONFIG="$(pwd)/llvm-config"

popd


%install
%{make_install} \
  PREFIX="%{_prefix}" \
  HELPER_PATH="%{afl_helper_path}" \
  DOC_PATH="%{_pkgdocdir}" \
  MISC_PATH="%{_pkgdocdir}"

# Otherwise we see:
# ERROR: No build ID note found in <.o file>
chmod -x $RPM_BUILD_ROOT%{afl_helper_path}/*.o


%check
# This just checks that simple programs can be compiled using
# the compiler wrappers.
ln -s %{SOURCE1} hello.cpp
./afl-gcc %{SOURCE1} -o hello
./hello
./afl-g++ hello.cpp -o hello
./hello
./afl-clang %{SOURCE1} -o hello
./hello
./afl-clang++ hello.cpp -o hello
./hello
./afl-clang-fast %{SOURCE1} -o hello
./hello
./afl-clang-fast++ hello.cpp -o hello
./hello


%files
%doc docs/*
%doc dictionaries/
%doc experimental/
%doc testcases/
%{_bindir}/afl-analyze
%{_bindir}/afl-fuzz
%{_bindir}/afl-gcc
%{_bindir}/afl-g++
%{_bindir}/afl-plot
%{_bindir}/afl-showmap
%{_bindir}/afl-tmin
%{_bindir}/afl-cmin
%{_bindir}/afl-gotcpu
%{_bindir}/afl-whatsup
%dir %{afl_helper_path}
%{afl_helper_path}/afl-as
%{afl_helper_path}/as


%files clang
%doc docs/COPYING
%{_bindir}/afl-clang
%{_bindir}/afl-clang++


%files clang-fast
%doc docs/COPYING llvm_mode/README.llvm
%{_bindir}/afl-clang-fast
%{_bindir}/afl-clang-fast++
%{afl_helper_path}/afl-llvm-pass.so
%if 0%{?__isa_bits} == 32
%{afl_helper_path}/afl-llvm-rt-32.o
%else
%{afl_helper_path}/afl-llvm-rt-64.o
%endif
%{afl_helper_path}/afl-llvm-rt.o


%changelog
* Sat Nov 03 2018 Richard W.M. Jones <rjones@redhat.com> - 2.52b-6
- Rebuild against new clang 7.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.52b-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Richard W.M. Jones <rjones@redhat.com> - 2.52b-4
- Depend on clang(major) exact version (see RHBZ#1547444 RHBZ#1544964).
- Fix C++ flags passed to clang++ to remove GCC-isms.

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 2.52b-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.52b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Richard W.M. Jones <rjones@redhat.com> - 2.52b-1
- New upstream version 2.52b (RHBZ#1509729).

* Tue Sep 12 2017 Richard W.M. Jones <rjones@redhat.com> - 2.51b-1
- New upstream version 2.51b (RHBZ#1487190).

* Tue Aug 22 2017 Richard W.M. Jones <rjones@redhat.com> - 2.50b-1
- New upstream version 2.50b (RHBZ#1483318).

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49b-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Richard W.M. Jones <rjones@redhat.com> - 2.49b-1
- New upstream version 2.49b (RHBZ#1472016).

* Fri Jul 14 2017 Richard W.M. Jones <rjones@redhat.com> - 2.47b-1
- New upstream version 2.47b (RHBZ#1470893).

* Tue Jul 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.46b-1
- New upstream version 2.46b (RHBZ#1467746).

* Thu Jun 29 2017 Richard W.M. Jones <rjones@redhat.com> - 2.44b-1
- New upstream version 2.44b (RHBZ#1458261).

* Thu Apr 13 2017 Richard W.M. Jones <rjones@redhat.com> - 2.41b-4
- New upstream version 2.41b (RHBZ#1441654).
- Fix Source URL.
- Compile afl-clang-fast (in a new subpackage).
- Add a simple check section.

* Tue Apr  4 2017 Richard W.M. Jones <rjones@redhat.com> - 2.40b-1
- New upstream version 2.40b (RHBZ#1418875).

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.38b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Richard W.M. Jones <rjones@redhat.com> - 2.38b-1
- New upstream version 2.38b (RHBZ#1376789).

* Sat Aug 27 2016 Richard W.M. Jones <rjones@redhat.com> - 2.33b-3
- New upstream version 2.33b (RHBZ#1350795).
- Remove patch.

* Fri Jun 24 2016 Richard W.M. Jones <rjones@redhat.com> - 2.16b-1
- New upstream version 2.16b (RHBZ#1336154).

* Wed May 04 2016 Richard W.M. Jones <rjones@redhat.com> - 2.12b-1
- New upstream version 2.12b (RHBZ#1331192).

* Thu Mar 31 2016 Richard W.M. Jones <rjones@redhat.com> - 2.10b-1
- New upstream version 2.10b (RHBZ#1317205).

* Tue Mar 08 2016 Richard W.M. Jones <rjones@redhat.com> - 2.07b-1
- New upstream version 2.07b (RHBZ#1311776).

* Mon Feb 22 2016 Richard W.M. Jones <rjones@redhat.com> - 2.04b-1
- New upstream version 2.04b (RHBZ#1310407).

* Thu Feb 18 2016 Richard W.M. Jones <rjones@redhat.com> - 2.02b-1
- New upstream version 2.02b (RHBZ#1309139).
- Remove afl-as, packaged in error.

* Mon Feb 15 2016 Richard W.M. Jones <rjones@redhat.com> - 2.00b-1
- New upstream version 2.00b (RHBZ#1306060).
- Rebase CFLAGS override patch.
- New programs afl-analyze, afl-as.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.96b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 Richard W.M. Jones <rjones@redhat.com> - 1.96b-1
- New upstream version 1.96b (RHBZ#1292637).

* Tue Nov 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.95b-1
- New upstream version 1.95b (RHBZ#1262537).

* Wed Sep  9 2015 Richard W.M. Jones <rjones@redhat.com> - 1.93b-1
- New upstream version 1.93b (RHBZ#1259960).

* Thu Sep  3 2015 Richard W.M. Jones <rjones@redhat.com> - 1.90b-1
- New upstream version 1.90b.

* Mon Aug 31 2015 Pádraig Brady <pbrady@redhat.com> - 1.88b-1
- Latest upstream

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.71b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Richard W.M. Jones <rjones@redhat.com> - 1.71b-1
- New upstream version 1.71b.

* Tue Feb 10 2015 Richard W.M. Jones <rjones@redhat.com> - 1.42b-1
- New upstream version 1.42b.
- Remove trademarked image from source (RHBZ#1191184).
- Use wildcard in .gitignore file.

* Sat Feb  7 2015 Richard W.M. Jones <rjones@redhat.com> - 1.40b-1
- New upstream version 1.40b (RHBZ#1188782).

* Tue Feb 03 2015 Pádraig Brady <pbrady@redhat.com> - 1.38b-1
- Latest upstream

* Mon Jan 26 2015 Pádraig Brady <pbrady@redhat.com> - 1.28b-1
- Latest upstream

* Thu Jan 22 2015 Pádraig Brady <pbrady@redhat.com> - 1.19b-1
- Latest upstream

* Mon Jan 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1.15b-1
- New upstream version 1.15b (RHBZ#1177434).

* Tue Dec 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.98b-1
- New upstream version 0.98b (RHBZ#1172581).
- Rename afl-plot.sh script to afl-plot.

* Mon Dec  8 2014 Richard W.M. Jones <rjones@redhat.com> - 0.88b-1
- New upstream version 0.88b (RHBZ#1170943).
- Add afl-plot.sh script.  This requires gnuplot, but it gives a
  suitable error message if gnuplot is not installed, so don't
  add a dependency.

* Sun Nov 30 2014 Pádraig Brady <pbrady@redhat.com> - 0.78b-1
- Latest upstream

* Mon Nov 17 2014 Richard W.M. Jones <rjones@redhat.com> - 0.50b-2
- Don't use epoch in requires.

* Sun Nov 16 2014 Richard W.M. Jones <rjones@redhat.com> - 0.50b-1
- New upstream version 0.50b.
- Remove 'sed' dependency as it is no longer used.
- Rebase CFLAGS patch.
- Add clang wrapper as a subpackage.

* Sat Nov 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.48b-1
- New upstream version 0.48b.
- Fix: https://code.google.com/p/american-fuzzy-lop/issues/detail?id=13

* Sat Nov 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.47b-1
- New upstream version 0.47b.
- Use stable Source URL.
- Remove parallel fix which is now upstream.

* Fri Nov 14 2014 Richard W.M. Jones <rjones@redhat.com> - 0.46b-1
- New upstream version 0.46b.
- Ditch USE_64BIT/CONF_64BIT.
- Package now owns afl_helper_path.
- Parallel builds now work, and make uses _smp_mflags.
- Uses CFLAGS optflags.
- Include (some) experimental scripts.

* Thu Nov 13 2014 Richard W.M. Jones <rjones@redhat.com> - 0.45b-1
- Initial packaging of afl.
