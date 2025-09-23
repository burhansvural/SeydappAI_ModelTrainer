# src/models/utils/validation.py
"""Parameter validation utilities"""
import torch
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ParameterValidator:
    """Training parameter validation and optimization"""

    @staticmethod
    def validate_training_parameters(
            training_args: Dict[str, Any],
            rtx3060_detected: bool = False
    ) -> Dict[str, Any]:
        """
        Validate and optimize training parameters
        RTX 3060 specific adjustments
        """
        validated_args = training_args.copy()

        # RTX 3060 specific validations
        if rtx3060_detected:
            validated_args = ParameterValidator._apply_rtx3060_optimizations(validated_args)

        # General validations
        validated_args = ParameterValidator._apply_general_validations(validated_args)

        logger.info("✅ Training parameters validated")
        return validated_args

    @staticmethod
    def _apply_rtx3060_optimizations(args: Dict[str, Any]) -> Dict[str, Any]:
        """Apply RTX 3060 specific parameter optimizations"""
        # Force small batch size
        if args.get('per_device_train_batch_size', 1) > 1:
            args['per_device_train_batch_size'] = 1
            logger.info("🔧 RTX 3060: Batch size limited to 1")

        # Increase gradient accumulation for effective batch size
        if args.get('gradient_accumulation_steps', 1) < 4:
            args['gradient_accumulation_steps'] = 8
            logger.info("🔧 RTX 3060: Gradient accumulation increased")

        # Force gradient checkpointing
        args['gradient_checkpointing'] = True
        logger.info("🔧 RTX 3060: Gradient checkpointing enabled")

        # Use bfloat16 for RTX 3060
        args['bf16'] = True
        args['fp16'] = False
        logger.info("🔧 RTX 3060: BFloat16 enabled")

        return args

    @staticmethod
    def _apply_general_validations(args: Dict[str, Any]) -> Dict[str, Any]:
        """Apply general parameter validations"""
        # Learning rate validation
        lr = args.get('learning_rate', 2e-4)
        if lr > 1e-3:
            args['learning_rate'] = 1e-3
            logger.warning("⚠️ Learning rate capped at 1e-3")
        elif lr < 1e-6:
            args['learning_rate'] = 1e-5
            logger.warning("⚠️ Learning rate increased to 1e-5")

        # Steps validation
        max_steps = args.get('max_steps', 50)
        if max_steps > 100:
            args['max_steps'] = 100
            logger.warning("⚠️ Max steps capped at 100")

        return args

    @staticmethod
    def validate_training_data(examples: List[Dict[str, Any]]) -> bool:
        """Validate training data format and content"""
        if not examples:
            logger.error("❌ No training examples provided")
            return False

        valid_examples = 0
        for i, example in enumerate(examples):
            if ParameterValidator._is_valid_example(example):
                valid_examples += 1
            else:
                logger.warning(f"⚠️ Invalid example at index {i}: {example}")

        if valid_examples == 0:
            logger.error("❌ No valid training examples found")
            return False

        logger.info(f"✅ Validated {valid_examples}/{len(examples)} training examples")
        return True

    @staticmethod
    def _is_valid_example(example: Dict[str, Any]) -> bool:
        """Check if single example is valid"""
        # Check for required fields
        if 'text' in example:
            return isinstance(example['text'], str) and len(example['text'].strip()) > 0
        elif 'input' in example and 'output' in example:
            return (isinstance(example['input'], str) and
                    isinstance(example['output'], str) and
                    len(example['input'].strip()) > 0 and
                    len(example['output'].strip()) > 0)

        return False
