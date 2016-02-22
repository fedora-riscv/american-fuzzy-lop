Name:          american-fuzzy-lop
Version:       2.04b
Release:       1%{?dist}

Summary:       Practical, instrumentation-driven fuzzer for binary formats

License:       ASL 2.0

URL:           http://lcamtuf.coredump.cx/afl/

Source0:       afl-%{version}.tgz

# Allow CFLAGS to be appended.
Patch1:        afl-2.00b-override-cflags.patch

# Upstream includes armv7hl support as some non-integrated 'contrib'
# files, so I have not enabled it here.  No other arch is supported
# without arch-specific changes.
ExclusiveArch: %{ix86} x86_64

BuildRequires: clang

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
Requires:      clang


%description clang
This subpackage contains clang and clang++ support for
%{name}.


%prep
%setup -q -n afl-%{version}

%patch1 -p1


%build
%{__make} %{?_smp_mflags} \
  CFLAGS="%{optflags}" \
  PREFIX=%{_prefix} \
  HELPER_PATH=%{afl_helper_path} \
  DOC_PATH=%{_pkgdocdir}


%install
%make_install \
  PREFIX=%{_prefix} \
  HELPER_PATH=%{afl_helper_path} \
  DOC_PATH=%{_pkgdocdir} \
  MISC_PATH=%{_pkgdocdir}


%files
%doc docs/*
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


%changelog
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
