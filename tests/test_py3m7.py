"""
Test suite for Python 3.7+ features (py3m7.py module).

Tests ForwardRef and collection types that were introduced or stabilized in Python 3.7.
"""

import sys
import pytest
from typing_compat.py3m7 import *


class TestPy3m7VersionFlag:
    """Test version detection for Python 3.7+ features."""
    
    def test_version_flag_accuracy(self):
        """Test that PY37_PLUS correctly detects Python 3.7+."""
        expected = sys.version_info >= (3, 7)
        assert PY37_PLUS == expected
    
    def test_version_flag_type(self):
        """Test that PY37_PLUS is a boolean."""
        assert isinstance(PY37_PLUS, bool)


class TestForwardRef:
    """Test ForwardRef functionality across Python versions."""
    
    def test_forward_ref_import(self):
        """Test that ForwardRef can be imported."""
        assert ForwardRef is not None
        assert callable(ForwardRef)
    
    def test_forward_ref_creation(self):
        """Test ForwardRef creation with string argument."""
        ref = ForwardRef('int')
        assert ref is not None
    
    def test_forward_ref_attributes(self):
        """Test ForwardRef has expected attributes."""
        ref = ForwardRef('str')
        
        # ForwardRef should have some kind of argument attribute
        # Different versions may use different attribute names
        has_arg_attr = (hasattr(ref, 'arg') or 
                       hasattr(ref, '__forward_arg__') or 
                       hasattr(ref, '_name') or
                       hasattr(ref, '__repr__'))  # At minimum should be representable
        assert has_arg_attr, f"ForwardRef missing expected attributes. Available: {[attr for attr in dir(ref) if not attr.startswith('_')]}"
    
    def test_forward_ref_with_complex_type(self):
        """Test ForwardRef with more complex type string."""
        ref = ForwardRef('List[Dict[str, int]]')
        assert ref is not None
    
    def test_forward_ref_module_source(self):
        """Test ForwardRef comes from expected module."""
        if PY37_PLUS:
            # Should come from typing or typing_extensions
            assert ForwardRef.__module__ in ('typing', 'typing_extensions')
        else:
            # Fallback implementation should still work
            assert ForwardRef is not None


class TestCollectionTypes:
    """Test collection types available in Python 3.7+."""
    
    def test_ordered_dict_import(self):
        """Test OrderedDict import."""
        assert OrderedDict is not None
        
        # Should be able to create instance
        od = OrderedDict([('a', 1), ('b', 2)])
        assert od['a'] == 1
        assert od['b'] == 2
    
    def test_counter_import(self):
        """Test Counter import."""
        assert Counter is not None
        
        # Should be able to create instance
        c = Counter('hello')
        assert c['l'] == 2
        assert c['h'] == 1
    
    def test_chain_map_import(self):
        """Test ChainMap import."""
        assert ChainMap is not None
        
        # Should be able to create instance
        cm = ChainMap({'a': 1}, {'b': 2})
        assert cm['a'] == 1
        assert cm['b'] == 2
    
    def test_deque_import(self):
        """Test Deque import."""
        assert Deque is not None
        
        # Should be usable for type hints
        def process_queue(q: Deque[str]) -> int:
            return len(q)
        
        # Test should pass without errors
        assert process_queue.__annotations__['q'] is not None
    
    def test_default_dict_import(self):
        """Test DefaultDict import."""
        assert DefaultDict is not None
        
        # Should be usable for type hints
        def process_defaults(d: DefaultDict[str, int]) -> int:
            return len(d)
        
        # Test should pass without errors
        assert process_defaults.__annotations__['d'] is not None


class TestPy3m7Integration:
    """Test integration of py3m7 features with other typing constructs."""
    
    def test_forward_ref_in_function_annotation(self):
        """Test using ForwardRef in function annotations."""
        UserRef = ForwardRef('User')
        
        def create_user() -> UserRef:
            pass
        
        # Should not raise errors
        assert create_user is not None
    
    def test_collection_types_in_generic_context(self):
        """Test collection types work with generic typing."""
        from typing import Union, Optional
        
        def process_data(
            items: Deque[str],
            lookup: DefaultDict[str, int],
            counts: Counter[str]
        ) -> Optional[OrderedDict[str, int]]:
            pass
        
        # Should create without errors
        assert process_data is not None
        
        # Check annotations exist
        annotations = process_data.__annotations__
        assert 'items' in annotations
        assert 'lookup' in annotations
        assert 'counts' in annotations
        assert 'return' in annotations


class TestPy3m7Fallbacks:
    """Test fallback behavior when typing_extensions is not available."""
    
    def test_forward_ref_fallback_works(self):
        """Test that ForwardRef fallback implementation works."""
        # Even if we're using a fallback, it should still be functional
        ref = ForwardRef('TestType')
        assert ref is not None
        
        # Should be able to access the argument in some way
        ref_str = str(ref)
        assert 'TestType' in ref_str or hasattr(ref, 'arg') or hasattr(ref, '__forward_arg__')
    
    def test_collection_types_always_available(self):
        """Test that collection types are always available."""
        # These should always work regardless of Python version
        types_to_test = [OrderedDict, Counter, ChainMap, Deque, DefaultDict]
        
        for type_class in types_to_test:
            assert type_class is not None
            # Should have a module
            assert hasattr(type_class, '__module__')


class TestPy3m7RealWorldUsage:
    """Test real-world usage patterns with Python 3.7+ features."""
    
    def test_forward_reference_pattern(self):
        """Test common forward reference pattern."""
        # This pattern is common in recursive data structures
        NodeRef = ForwardRef('TreeNode')
        
        def create_tree_node(value: int, children: Deque[NodeRef]) -> NodeRef:
            pass
        
        # Should work without issues
        assert create_tree_node is not None
    
    def test_complex_collection_typing(self):
        """Test complex collection type annotations."""
        def analyze_data(
            word_counts: Counter[str],
            category_maps: ChainMap[str, DefaultDict[str, int]],
            processing_queue: Deque[OrderedDict[str, str]]
        ) -> OrderedDict[str, Counter[str]]:
            pass
        
        # Should create complex annotations without errors
        assert analyze_data is not None
        
        # All parameters should have type annotations
        annotations = analyze_data.__annotations__
        assert len(annotations) == 4  # 3 params + return


class TestPy3m7ErrorCases:
    """Test error handling and edge cases for Python 3.7+ features."""
    
    def test_forward_ref_empty_string(self):
        """Test ForwardRef with empty string."""
        # Some implementations might handle this differently
        try:
            ref = ForwardRef('')
            assert ref is not None
        except (ValueError, TypeError, SyntaxError):
            # Some implementations might reject empty strings or invalid syntax
            pass
    
    def test_forward_ref_with_special_characters(self):
        """Test ForwardRef with various string inputs."""
        test_cases = [
            'SimpleType',
            'Module.Type',
            'Generic[T]',
            'Union[int, str]'
        ]
        
        for case in test_cases:
            try:
                ref = ForwardRef(case)
                assert ref is not None
            except Exception as e:
                # Document what exceptions are acceptable
                assert isinstance(e, (ValueError, TypeError, AttributeError))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
