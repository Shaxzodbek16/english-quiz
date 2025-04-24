import { toast } from "sonner";

// Load API base URL from environment or use default
export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Types for API responses
export interface LoginResponse {
  access_token: string;
  token_type: string;
  refresh_token: string;
}

export interface Level {
  name: string;
  image: string;
  id: number;
  created_at: string;
  updated_at: string;
}

export interface Topic {
  name: string;
  image: string;
  id: number;
  created_at: string;
  updated_at: string;
}

export interface TestOption {
  option: string;
  is_correct: boolean;
  id: number;
  created_at: string;
  updated_at: string;
}

export interface Test {
  level_id: number;
  topic_id: number;
  type_id: number;
  question: string;
  image: string;
  answer_explanation: string;
  id: number;
  options: TestOption[];
  created_at: string;
  updated_at: string;
}

// New types for user tests and statistics
export interface UserTestResult {
  test_id: number;
  selected_option_id: number;
  correct_option_id: number;
}

export interface UserStatistics {
  total_tests: number;
  correct_answers: number;
  incorrect_answers: number;
}

// Auth functions
export const login = async (userId: string): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/user/login/?user=${userId}`);
    
    if (!response.ok) {
      throw new Error(`Login failed: ${response.statusText}`);
    }
    
    const data: LoginResponse = await response.json();
    
    // Store tokens in localStorage
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("token_type", data.token_type);
    localStorage.setItem("user_id", userId);
    
    toast.success("Login successful");
    return true;
  } catch (error) {
    console.error("Login error:", error);
    toast.error("Login failed. Please try again.");
    return false;
  }
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("token_type");
  localStorage.removeItem("user_id");
  toast.success("Logged out successfully");
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem("access_token");
};

// API calls with auth headers
const authHeaders = (): HeadersInit => {
  const token = localStorage.getItem("access_token");
  const tokenType = localStorage.getItem("token_type") || "Bearer";
  
  return {
    "Authorization": `${tokenType} ${token}`,
    "Content-Type": "application/json",
  };
};

export const fetchLevels = async (): Promise<Level[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels/`, {
      headers: authHeaders(),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch levels: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching levels:", error);
    toast.error("Failed to load levels");
    return [];
  }
};

export const fetchTopics = async (): Promise<Topic[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/topics/`, {
      headers: authHeaders(),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch topics: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching topics:", error);
    toast.error("Failed to load topics");
    return [];
  }
};

export const fetchTests = async (levelId: number, topicId: number, typeId: number = 1, page: number = 1, size: number = 15): Promise<Test[]> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/tests/?level_id=${levelId}&topic_id=${topicId}&type_id=${typeId}&page=${page}&size=${size}`,
      {
        headers: authHeaders(),
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to fetch tests: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching tests:", error);
    toast.error("Failed to load tests");
    return [];
  }
};

// New API functions for user tests and statistics
export const submitTestResult = async (result: UserTestResult): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/user-tests/`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(result)
    });
    
    if (!response.ok) {
      throw new Error(`Failed to submit test result: ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error submitting test result:", error);
    toast.error("Failed to save test result");
    throw error;
  }
};
