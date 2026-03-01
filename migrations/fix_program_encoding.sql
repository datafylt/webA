-- Fix encoding for program table
-- Run this to update the French accents

UPDATE program SET 
    name = 'Licence C - Compagnon Électricien',
    description = 'Préparation complète à l''examen de qualification pour l''obtention de la Licence C d''Emploi-Québec.'
WHERE code = 'licence_c';

UPDATE program SET 
    name = 'RCA - Connexions Restreintes',
    description = 'Formation pour l''obtention du certificat de Raccordement et Connexions d''Appareillage électrique.'
WHERE code = 'rca';

UPDATE program SET 
    name = 'RBQ - Constructeur Propriétaire',
    description = 'Préparation aux examens de la RBQ pour les constructeurs-propriétaires.'
WHERE code = 'rbq';

UPDATE program SET 
    name = 'CMEQ - Entrepreneur Électricien',
    description = 'Formation préparatoire aux examens de la Corporation des maîtres électriciens du Québec.'
WHERE code = 'cmeq';

UPDATE program SET 
    name = 'Sceau Rouge - Interprovincial',
    description = 'Préparation à l''examen interprovincial Sceau Rouge pour électriciens.'
WHERE code = 'sceau_rouge';

UPDATE program SET 
    name = 'Formation sur mesure',
    description = 'Programmes personnalisés adaptés aux besoins spécifiques des entreprises et individus.'
WHERE code = 'custom';
