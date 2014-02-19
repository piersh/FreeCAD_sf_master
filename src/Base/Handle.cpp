/***************************************************************************
 *   (c) Jürgen Riegel (juergen.riegel@web.de) 2002                        *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Library General Public License (LGPL)   *
 *   as published by the Free Software Foundation; either version 2 of     *
 *   the License, or (at your option) any later version.                   *
 *   for detail see the LICENCE text file.                                 *
 *                                                                         *
 *   FreeCAD is distributed in the hope that it will be useful,            *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with FreeCAD; if not, write to the Free Software        *
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
 *   USA                                                                   *
 *                                                                         *
 *   Juergen Riegel 2002                                                   *
 ***************************************************************************/


#include "PreCompiled.h"

#ifndef _PreComp_
# include <assert.h>
#endif

#include <QAtomicInt>

#include "Handle.h"
#include "Exception.h"

using namespace Base;

//**************************************************************************
// Construction/Destruction

Handled::Handled()
  : _lRefCount(new QAtomicInt(0))
{
}

Handled::~Handled()
{
#if QT_VERSION >= 0x050000
    if (_lRefCount->load() != 0) 
#else
    if ((int)(*_lRefCount) != 0)
#endif
        throw Exception("Reference counter of deleted object is not zero!!!!!\n");
	
    delete _lRefCount;
}

void Handled::ref() const
{
    _lRefCount->ref();
}

void Handled::unref() const
{
    assert(_lRefCount > 0);
    if (!_lRefCount->deref()) {
        delete this;
    }
}

int Handled::getRefCount(void) const
{
#if QT_VERSION >= 0x050000
    return _lRefCount->load();
#else
    return (int)(*_lRefCount);
#endif
}

const Handled& Handled::operator = (const Handled&)
{
    // we must not assign _lRefCount
    return *this;
}
