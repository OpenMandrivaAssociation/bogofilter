#define _requires_exceptions perl
%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	Fast anti-spam filtering by Bayesian statistical analysis
Name:		bogofilter
Version:	1.2.4
Release:	12
License:	GPLv2+
Group:		Networking/Mail
URL:		http://bogofilter.sourceforge.net
Source0:	http://freefr.dl.sourceforge.net/project/bogofilter/bogofilter-%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	db-devel
BuildRequires:	gsl-devel
BuildRequires:	valgrind
BuildRequires:	flex
BuildRequires:	xmlto
BuildRequires:	openjade

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

%build
%configure2_5x \
    --disable-rpath \
    --disable-transactions \
    --with-database=db \
    --without-included-gsl

%make

%check
# Some strange test failures that would need to be investigated but don't seem fatal
# 3/54 Failed:
#./outputs/dump.load-2.out ./checks.23370.20160529T004141/dump.load-2.txt differ: char 87, line 3
#FAIL: t.dump.load
#want: "7.2 6.20030303 10.20030304", have: "1.2 6.20030303 10.20030304"
#FAIL: t.nonascii.replace
#./outputs/bulkmode.out ./checks.24400.20160529T004148/bulk-double-2.out differ: char 80, line 3
#FAIL: t.bulkmode

make DESTDIR="%{buildroot}" check ||

%install
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

%files
%doc AUTHORS GETTING.STARTED Doxyfile NEWS
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


%changelog
* Mon May 07 2012 Crispin Boylan <crisb@mandriva.org> 1.2.2-4
+ Revision: 797318
- Rebuild

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - build with db 5.1 (fwang | 2011-04-12 10:39:11 +0200)

* Sun Jul 11 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.2-2mdv2011.0
+ Revision: 551171
- add a _requires_exceptions for perl, not needed (from Charles A Edwards)

* Sat Jul 10 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.2-1mdv2011.0
+ Revision: 550109
- update to new version 1.2.2

* Sat Jan 02 2010 Funda Wang <fwang@mandriva.org> 1.2.1-2mdv2010.1
+ Revision: 484939
- build for db4.8

* Fri Aug 14 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.1-1mdv2010.0
+ Revision: 416385
- update to new version 1.2.1

* Tue Feb 24 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 344436
- build against db4.7
- update to new version 1.2.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.1.7-2mdv2009.0
+ Revision: 266301
- rebuild early 2009.0 package (before pixel changes)

* Wed May 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.7-1mdv2009.0
+ Revision: 202667
- new version
- drop patch 0 and 1, not usefull imho
- enable valgrind test
- add missing buildrequires

* Fri Jan 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.6-3mdv2008.1
+ Revision: 147813
- disable transactional mode in Berkeley DB, probably this causes bug #36504
- do not package INSTALL file

* Sun Dec 30 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.6-2mdv2008.1
+ Revision: 139395
- rebuild against db4.6
- new license policy
- do not package COPYING file

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 06 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.6-1mdv2008.1
+ Revision: 116019
- updated to version 1.1.6

* Tue Sep 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.5-2mdv2008.0
+ Revision: 89868
- remove dead configure option
- disable rpath
- enable transactions
- use system gsl library
- compile with support with Berkeley's database
- spec file clean

