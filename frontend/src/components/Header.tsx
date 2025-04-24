import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { Link } from "react-router-dom";

const Header = () => {
  const { isLoggedIn, logout } = useAuth();

  return (
    <header className="flex items-center justify-between border-b border-purple-200/20 bg-white/50 px-6 py-4 backdrop-blur-sm dark:bg-purple-950/50">
      <Link to="/" className="text-2xl font-bold text-purple-900 dark:text-purple-100">
        Card Game
      </Link>
      <div className="flex gap-4">
        {isLoggedIn && (
          <>
            <Link to="/profile">
              <Button variant="outline">Profile</Button>
            </Link>
            <Link to="/admin">
              <Button variant="outline">Admin</Button>
            </Link>
            <Button variant="outline">Options</Button>
            <Button variant="destructive" onClick={logout}>
              Logout
            </Button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
