Summary:	Fast anti-spam filtering by Bayesian statistical analysis
Name:		bogofilter
Version:	1.1.6
Release:	%mkrel 1
License:	GPL
Group:		Networking/Mail
URL:		http://bogofilter.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/bogofilter/%{name}-%{version}.tar.bz2 
Patch0:		%{name}-0.95.2-novalgrindtest.patch
Patch1:		%{name}-1.1.5-glibc.patch
BuildRequires:	db4.2-devel
BuildRequires:	gsl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Bogofilter is a Bayesian spam filter. In its normal mode of
operation, it takes an email message or other text on standard
input, does a statistical check against lists of "good" and
"bad" words, and returns a status code indicating whether or not
the message is spam. Bogofilter is designed with fast algorithms
(including Berkeley DB system), coded directly in C, and tuned for
speed, so it can be used for production by sites that process a
lot of mail.

%prep

%setup -q
%patch0 -p1 -b .novalgrindtest 
%patch1 -p1 -b .glibc

%build

%configure2_5x \
    --disable-rpath \
    --enable-transactions \
    --with-database=db \
    --without-included-gsl

%make
 

%check
make DESTDIR="%{buildroot}" check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

mv %{buildroot}%{_sysconfdir}/bogofilter.cf.example %{buildroot}%{_sysconfdir}/bogofilter.cf

##include contrib...some my find it usefull
for d in contrib ; do
  install -d %{buildroot}%{_datadir}/%{name}/$d
  files=$(find "$d" -maxdepth 1 -type f -print)
  for f in $files ; do
    case $f in
      *.c|*.o|*.obj|*/Makefile*) continue ;;
      *.1)
    cp -p $f %{buildroot}%{_mandir}/man1 ;;
      *)
    cp -p $f %{buildroot}%{_datadir}/%{name}/$d ;;
    esac
  done
done

# it gets built, so why not install it?
##it is only needed to run check during build and does not need to be installed CAE
#install -m755 contrib/bogogrep %{buildroot}%{_bindir}/

# prepare for doc inclusion
for n in xml html ; do
  install -d .inst/$n
  install -m644 doc/*.$n .inst/$n
done
 
%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING GETTING.STARTED Doxyfile INSTALL NEWS
%doc README* RELEASE.NOTES
%doc RELEASE.NOTES* TODO bogofilter.cf.example
%doc doc/README* doc/bogofilter-SA*
%doc doc/integrating-* 
%doc doc/rpm.notes.BerkeleyDB 
%doc .inst/html .inst/xml
%doc trio/AUTHORS trio/CHANGES trio/README 
%doc contrib/README*
%config(noreplace) %{_sysconfdir}/bogofilter.cf
%{_bindir}/*
%{_datadir}/bogofilter
%{_mandir}/man1/*
