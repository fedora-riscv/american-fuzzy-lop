Name:          american-fuzzy-lop
Version:       0.50b
Release:       2%{?dist}

Summary:       Practical, instrumentation-driven fuzzer for binary formats

License:       ASL 2.0

URL:           http://lcamtuf.coredump.cx/afl/
Source0:       http://lcamtuf.coredump.cx/afl/releases/afl-%{version}.tgz

# Allow CFLAGS to be appended.
Patch1:        afl-0.50b-override-cflags.patch

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
make %{_smp_mflags} \
    CFLAGS="%{optflags}" \
    BIN_PATH=%{_bindir} \
    HELPER_PATH=%{afl_helper_path} \
    all


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{afl_helper_path}
make \
    BIN_PATH=$RPM_BUILD_ROOT%{_bindir} \
    HELPER_PATH=$RPM_BUILD_ROOT%{afl_helper_path} \
    install


%files
%doc docs/*
%doc experimental/crash_triage
%doc experimental/distributed_fuzzing
%doc experimental/minimization_script
%{_bindir}/afl-fuzz
%{_bindir}/afl-gcc
%{_bindir}/afl-g++
%{_bindir}/afl-showmap
%dir %{afl_helper_path}
%{afl_helper_path}/afl-as
%{afl_helper_path}/as


%files clang
%doc docs/COPYING
%{_bindir}/afl-clang
%{_bindir}/afl-clang++


%changelog
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
