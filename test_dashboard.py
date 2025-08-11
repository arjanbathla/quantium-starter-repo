import pytest
import dash
from dash import html, dcc
from dash.testing.application_runners import import_app
import time

# Import the app
app = import_app("soul_foods_dashboard")

def search_layout_recursively(element, search_func):
    """
    Recursively search through the layout to find elements.
    """
    # Apply search function to current element
    search_func(element)
    
    # Recursively search children
    if hasattr(element, 'children'):
        if isinstance(element.children, list):
            for child in element.children:
                search_layout_recursively(child, search_func)
        elif element.children is not None:
            search_layout_recursively(element.children, search_func)

def test_header_present():
    """
    Test that the header is present in the app layout.
    """
    # Check that the app has a layout
    assert app.layout is not None
    
    # Check first child (header container)
    first_child = app.layout.children[0]
    
    # Check if H1 is in the first child's children
    header_found = False
    header_text = ""
    
    for child in first_child.children:
        if hasattr(child, '_type') and child._type == 'H1':
            header_found = True
            header_text = str(child.children)
            break
        elif 'H1' in str(type(child)):
            header_found = True
            header_text = str(child.children)
            break
    
    # Assert that header was found
    assert header_found, "Header (H1) element not found in app layout"
    assert "Soul Foods - Pink Morsels Sales Analysis Dashboard" in header_text, f"Expected header text not found. Found: {header_text}"
    assert "🍪" in header_text, "Header emoji not found"
    
    print("✅ Header test passed - Header is present and contains expected text")

def test_visualization_present():
    """
    Test that the visualization (chart) is present in the app layout.
    """
    # Check that the app has a layout
    assert app.layout is not None
    
    # Find the chart element in the layout
    chart_found = False
    chart_container_found = False
    
    def search_for_chart(element):
        nonlocal chart_found, chart_container_found
        if hasattr(element, '_type') and element._type == 'Graph':
            chart_found = True
        
        if hasattr(element, '_type') and element._type == 'H4':
            if hasattr(element, 'children') and "📊 Sales Performance Over Time" in str(element.children):
                chart_container_found = True
    
    search_layout_recursively(app.layout, search_for_chart)
    
    # Assert that chart was found
    assert chart_found, "Chart (Graph) element not found in app layout"
    assert chart_container_found, "Chart container header not found"
    
    print("✅ Visualization test passed - Chart is present in app layout")

def test_region_picker_present():
    """
    Test that the region picker (radio buttons) is present in the app layout.
    """
    # Check that the app has a layout
    assert app.layout is not None
    
    # Find the region picker element in the layout
    radio_items_found = False
    region_label_found = False
    
    def search_for_region_picker(element):
        nonlocal radio_items_found, region_label_found
        if hasattr(element, '_type') and element._type == 'RadioItems':
            radio_items_found = True
            # Check that it has the expected options
            if hasattr(element, 'options'):
                expected_values = ['all', 'north', 'south', 'east', 'west']
                actual_values = [opt['value'] for opt in element.options]
                assert actual_values == expected_values, f"Expected radio button values {expected_values}, got {actual_values}"
        
        if hasattr(element, '_type') and element._type == 'Label':
            if hasattr(element, 'children') and "🌍 Filter by Region:" in str(element.children):
                region_label_found = True
    
    search_layout_recursively(app.layout, search_for_region_picker)
    
    # Assert that region picker was found
    assert radio_items_found, "RadioItems element not found in app layout"
    assert region_label_found, "Region filter label not found"
    
    print("✅ Region picker test passed - Radio buttons are present and functional")

def test_app_layout_structure():
    """
    Test that the app layout has the expected structure and components.
    """
    # Check that the app has a layout
    assert app.layout is not None
    
    # Check for business question section
    business_question_found = False
    date_picker_found = False
    summary_stats_found = False
    business_insight_found = False
    
    def search_for_components(element):
        nonlocal business_question_found, date_picker_found, summary_stats_found, business_insight_found
        
        if hasattr(element, '_type') and element._type == 'H3':
            if hasattr(element, 'children') and "Business Question:" in str(element.children):
                business_question_found = True
        
        if hasattr(element, '_type') and element._type == 'DatePickerRange':
            date_picker_found = True
        
        if hasattr(element, '_type') and element._type == 'H4':
            if hasattr(element, 'children'):
                children_str = str(element.children)
                if "📈 Summary Statistics" in children_str:
                    summary_stats_found = True
                elif "💡 Business Insight" in children_str:
                    business_insight_found = True
    
    search_layout_recursively(app.layout, search_for_components)
    
    # Assert that all components were found
    assert business_question_found, "Business question section not found"
    assert date_picker_found, "Date picker not found"
    assert summary_stats_found, "Summary statistics section not found"
    assert business_insight_found, "Business insight section not found"
    
    print("✅ Layout structure test passed - All major components are present")

def test_app_import():
    """
    Test that the app can be imported and has the expected structure.
    """
    # Test that app is a Dash app
    assert isinstance(app, dash.Dash)
    
    # Test that app has a layout
    assert hasattr(app, 'layout')
    assert app.layout is not None
    
    # Test that app has callbacks
    assert hasattr(app, 'callback_map')
    
    print("✅ App import test passed - App structure is correct")

if __name__ == "__main__":
    # Run tests
    print("🧪 Running Soul Foods Dashboard Test Suite...")
    print("=" * 50)
    
    try:
        test_app_import()
        test_header_present()
        test_visualization_present()
        test_region_picker_present()
        test_app_layout_structure()
        
        print("=" * 50)
        print("🎉 All tests passed! Dashboard is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise 