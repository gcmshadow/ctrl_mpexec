# This file is part of ctrl_mpexec.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['ExecutionGraphFixup']

from abc import ABC, abstractmethod
from typing import Iterable

from lsst.pipe.base import QuantumIterData


class ExecutionGraphFixup(ABC):
    """Interface for classes which update quantum graphs before execution.

    Primary goal of this class is to modify quanta dependencies which may
    not be possible to reflect in a quantum graph using standard tools.
    One known use case for that is to guarantee particular execution order
    of visits in CI jobs for cases when outcome depends on the processing
    order of visits (e.g. AP association pipeline).

    Instances of this class receive pre-ordered sequence of quanta
    (`~lsst.pipe.base.QuantumIterData` instances) and they are allowed to
    modify quanta data in place, for example update ``dependencies`` field to
    add additional dependencies. Returned list of quanta will be re-ordered
    once again by the graph executor to reflect new dependencies.
    """

    @abstractmethod
    def fixupQuanta(self, quanta: Iterable[QuantumIterData]) -> Iterable[QuantumIterData]:
        """Update quanta in a graph.

        Potentially anything in the graph could be changed if it does not
        break executor assumptions. Returned quanta will be re-ordered by
        executor, if modifications result in a dependency cycle the executor
        will raise an exception.

        Parameters
        ----------
        quanta : iterable [`~lsst.pipe.base.QuantumIterData`]
            Iterable of topologically ordered quanta as returned from
            `lsst.pipe.base.QuantumGraph.traverse` method.

        Yields
        ------
        quantum : `~lsst.pipe.base.QuantumIterData`
        """
        raise NotImplementedError