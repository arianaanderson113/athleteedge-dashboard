"""
AthleteEdge AI - Automated Evaluation Script

This script runs automated tests against the AthleteEdge AI system
to evaluate response accuracy, privacy enforcement, response time, and citation inclusion.

Usage:
    python evaluation_script.py

Requirements:
    - AthleteEdge server running at localhost:5000
    - Valid Gemini API key initialized in the system
"""

import json
import time
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_ENDPOINT = f"{BASE_URL}/api/query"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"

# Load test cases
with open('evaluation_test_cases.json', 'r') as f:
    test_data = json.load(f)
    TEST_CASES = test_data['test_cases']
    EXPECTED_RESULTS = test_data['expected_results']

# Results storage
results = {
    'total_tests': len(TEST_CASES),
    'passed': 0,
    'failed': 0,
    'blocked_correctly': 0,
    'privacy_violations': 0,
    'total_response_time': 0,
    'citations_found': 0,
    'citations_expected': 0,
    'test_details': []
}

def login(username, password):
    """Authenticate and get session"""
    response = requests.post(LOGIN_ENDPOINT, json={
        'username': username,
        'password': password
    })
    return response.cookies if response.status_code == 200 else None

def run_query(query, cookies):
    """Execute a query against the API"""
    start_time = time.time()
    response = requests.post(API_ENDPOINT, json={'query': query}, cookies=cookies)
    response_time = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        return {
            'status': data.get('status'),
            'message': data.get('message', ''),
            'response_time': response_time,
            'success': True
        }
    else:
        return {
            'status': 'error',
            'message': 'Request failed',
            'response_time': response_time,
            'success': False
        }

def check_privacy_block(response):
    """Check if response indicates privacy block"""
    blocked_messages = ['⚠️', 'blocked', 'cannot', 'not allowed', 'Students can only view their own data']
    message = response.get('message', '').lower()
    return any(msg.lower() in message for msg in blocked_messages)

def check_citation(response):
    """Check if response contains research citations"""
    citation_keywords = ['ajsm', 'jospt', 'bjsm', 'research', 'study', 'protocol', 'according to']
    message = response.get('message', '').lower()
    return any(keyword in message for keyword in citation_keywords)

def check_expected_data(response, expected_data):
    """Check if response contains expected data elements"""
    message = response.get('message', '').lower()
    return all(data.lower() in message for data in expected_data)

def run_evaluation():
    """Run all test cases and collect results"""
    print("=" * 60)
    print("ATHLETEEDGE AI - AUTOMATED EVALUATION")
    print("=" * 60)
    print(f"\nRunning {len(TEST_CASES)} test cases...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for test_case in TEST_CASES:
        test_id = test_case['id']
        role = test_case['role']
        username = test_case['username']
        password = "Password123!" if role == "student" else "Coach456#"
        query = test_case['query']
        expected_block = test_case.get('expected_block', False)
        expect_citation = test_case.get('expect_citation', False)
        expect_data = test_case.get('expect_data', [])
        
        print(f"Test {test_id}: {test_case['test_type']}")
        print(f"  Role: {role}")
        print(f"  Query: {query}")
        
        # Login
        cookies = login(username, password)
        if not cookies:
            print(f"  ❌ Login failed for {username}")
            results['failed'] += 1
            continue
        
        # Run query
        response = run_query(query, cookies)
        
        # Evaluate response
        test_result = {
            'test_id': test_id,
            'query': query,
            'role': role,
            'response_time': response['response_time'],
            'passed': False,
            'reason': ''
        }
        
        # Check if should be blocked
        if expected_block:
            is_blocked = check_privacy_block(response)
            if is_blocked:
                print(f"  ✅ Correctly blocked")
                results['blocked_correctly'] += 1
                results['passed'] += 1
                test_result['passed'] = True
                test_result['reason'] = 'Privacy block working correctly'
            else:
                print(f"  ❌ Should have blocked but didn't")
                results['privacy_violations'] += 1
                results['failed'] += 1
                test_result['reason'] = 'Privacy violation - query not blocked'
        else:
            # Check success
            if not response['success']:
                print(f"  ❌ Query failed")
                results['failed'] += 1
                test_result['reason'] = 'Query failed to execute'
            else:
                # Check expected data
                if expect_data:
                    has_data = check_expected_data(response, expect_data)
                    if has_data:
                        print(f"  ✅ Contains expected data")
                        results['passed'] += 1
                        test_result['passed'] = True
                        test_result['reason'] = 'Response contains expected data'
                    else:
                        print(f"  ⚠️  Missing expected data: {expect_data}")
                        results['failed'] += 1
                        test_result['reason'] = f'Missing expected data: {expect_data}'
                else:
                    print(f"  ✅ Query executed successfully")
                    results['passed'] += 1
                    test_result['passed'] = True
                    test_result['reason'] = 'Query successful'
                
                # Check citation if expected
                if expect_citation:
                    results['citations_expected'] += 1
                    has_citation = check_citation(response)
                    if has_citation:
                        results['citations_found'] += 1
                        print(f"  📚 Citation found")
                    else:
                        print(f"  ⚠️  Citation missing")
        
        # Record response time
        results['total_response_time'] += response['response_time']
        test_result['message_preview'] = response['message'][:100] + '...' if len(response['message']) > 100 else response['message']
        results['test_details'].append(test_result)
        
        print(f"  ⏱️  Response time: {response['response_time']:.2f}s\n")
    
    # Calculate metrics
    avg_response_time = results['total_response_time'] / results['total_tests']
    accuracy = (results['passed'] / results['total_tests']) * 100
    privacy_enforcement = (results['blocked_correctly'] / sum(1 for tc in TEST_CASES if tc.get('expected_block'))) * 100
    citation_rate = (results['citations_found'] / results['citations_expected'] * 100) if results['citations_expected'] > 0 else 0
    
    # Print summary
    print("=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"\nTotal Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']} ({accuracy:.1f}%)")
    print(f"Failed: {results['failed']}")
    print(f"\nPrivacy Enforcement: {results['blocked_correctly']}/{sum(1 for tc in TEST_CASES if tc.get('expected_block'))} ({privacy_enforcement:.1f}%)")
    print(f"Privacy Violations: {results['privacy_violations']}")
    print(f"\nAverage Response Time: {avg_response_time:.2f}s")
    print(f"Citation Inclusion: {results['citations_found']}/{results['citations_expected']} ({citation_rate:.1f}%)")
    
    # Compare to expected results
    print(f"\n{'METRIC':<30} {'EXPECTED':<15} {'ACTUAL':<15} {'STATUS'}")
    print("-" * 70)
    
    acc_status = "✅" if accuracy >= 95 else "⚠️"
    print(f"{'Response Accuracy':<30} {'>=95%':<15} {f'{accuracy:.1f}%':<15} {acc_status}")
    
    priv_status = "✅" if privacy_enforcement == 100 else "❌"
    print(f"{'Privacy Enforcement':<30} {'100%':<15} {f'{privacy_enforcement:.1f}%':<15} {priv_status}")
    
    time_status = "✅" if avg_response_time < 3 else "⚠️"
    print(f"{'Avg Response Time':<30} {'<3s':<15} {f'{avg_response_time:.2f}s':<15} {time_status}")
    
    cite_status = "✅" if citation_rate >= 80 else "⚠️"
    print(f"{'Citation Inclusion':<30} {'>=80%':<15} {f'{citation_rate:.1f}%':<15} {cite_status}")
    
    print("\n" + "=" * 60)
    
    # Save detailed results
    output = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': results['total_tests'],
            'passed': results['passed'],
            'failed': results['failed'],
            'accuracy_percent': accuracy,
            'privacy_enforcement_percent': privacy_enforcement,
            'avg_response_time': avg_response_time,
            'citation_rate_percent': citation_rate
        },
        'test_details': results['test_details']
    }
    
    with open('evaluation_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nDetailed results saved to: evaluation_results.json")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        print("\n⚠️  IMPORTANT: Make sure AthleteEdge server is running at localhost:5000")
        print("⚠️  And that you've initialized the system with a valid Gemini API key\n")
        input("Press Enter to start evaluation...")
        run_evaluation()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to localhost:5000")
        print("Make sure the AthleteEdge server is running!")
        print("Run: python athleteedge_final.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
