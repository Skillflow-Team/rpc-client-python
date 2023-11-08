===================
Models
===================

Overview
========
.. automodule:: core.models


Objective
=========

.. automodule:: core.models.objective

.. autoclass:: core.models.objective.Objective
   :show-inheritance:


Grading Criteria
================

.. automodule:: core.models.grading_criteria

.. autoclass:: core.models.grading_criteria.GradingCriteria
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: model_config, model_fields, objective, weight, validate_weight

Rubric
======

.. automodule:: core.models.rubric

.. autoclass:: core.models.rubric.RubricType
   :show-inheritance:
   :members:
   :exclude-members: FACTUAL_RUBRIC, ANALYTICAL_RUBRIC, CREATIVE_RUBRIC, COMPREHENSIVE_RUBRIC, COMMUNICATION_RUBRIC, CUSTOM_RUBRIC

.. autoclass:: core.models.rubric.Rubric
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: rubric_type, size, criteria

Short Answer Question
=====================

.. automodule:: core.models.short_answer

.. autoclass:: core.models.short_answer.ShortAnswerQuestion
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: body, example_answer, rubric
