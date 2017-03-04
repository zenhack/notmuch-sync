notmuch-sync
============

``notmuch-sync`` is a toolbox for syncronizing mail setups of `notmuch
<https://notmuchmail.org/>`_. Right now all it contains is a 3-way
merge tool for the output of ``notmuch-dump(1)``:

::

	usage: notmuch-sync <ancestor> <left> <right> <result>

I use this in conjunction with git to synchronize my tags. In ``~/.gitconfig``:

::

	[merge "notmuchtags"]
		name = Notmuch tag merge driver
		driver = notmuch-sync %O %B %A %A
		recursive = binary

And then in ``.gitattributes`` at the root of the repo:

::

	_tagsdump merge=notmuchtags

Where _tagsdump generated from ``notmuch-dump`` before each commit/merge, and
restored with ``notmuch-restore`` after the merge.

The downside with this is that it expects a full list of tags, which can get
slow to import/export when there's a lot of mail. I intend to solve this
problem soonish.

License
-------

::

	Copyright (C) 2017 Ian Denhardt <ian@zenhack.net>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
