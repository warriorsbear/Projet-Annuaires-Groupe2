"""
Package annuaire - Classes métier pour la gestion d'annuaires.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

from .Client import Client
from .Administrateur import Administrateur
from .Annuaire import Annuaire

__all__ = ['Client', 'Administrateur', 'Annuaire']

