
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { login as apiLogin, logout as apiLogout, isAuthenticated } from "../services/api";
import { useNavigate } from "react-router-dom";

type AuthContextType = {
  isLoggedIn: boolean;
  user: string | null;
  login: (userId: string) => Promise<boolean>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(isAuthenticated());
  const [user, setUser] = useState<string | null>(localStorage.getItem("user_id"));
  const navigate = useNavigate();

  useEffect(() => {
    // Check authentication status on mount
    const checkAuth = () => {
      const authenticated = isAuthenticated();
      setIsLoggedIn(authenticated);
      setUser(localStorage.getItem("user_id"));
    };

    checkAuth();
    // Listen for storage events (for multi-tab logout)
    window.addEventListener("storage", checkAuth);

    return () => {
      window.removeEventListener("storage", checkAuth);
    };
  }, []);

  const login = async (userId: string): Promise<boolean> => {
    const success = await apiLogin(userId);
    if (success) {
      setIsLoggedIn(true);
      setUser(userId);
      navigate("/levels");
    }
    return success;
  };

  const logout = () => {
    apiLogout();
    setIsLoggedIn(false);
    setUser(null);
    navigate("/");
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
