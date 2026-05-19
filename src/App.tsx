import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import FridgePage from './pages/FridgePage';
import RecipesPage from './pages/RecipesPage';
import RecipeDetailPage from './pages/RecipeDetailPage';
import PreferencesPage from './pages/PreferencesPage';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import ShoppingListPage from './pages/ShoppingListPage';
import { FridgeProvider } from './store/FridgeContext';
import { AuthProvider } from './store/AuthContext';
import { RecipeProvider } from './store/RecipeContext';
import { ShoppingListProvider } from './store/ShoppingListContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <FridgeProvider>
        <ShoppingListProvider>
        <RecipeProvider>
          <Router>
              <div className="min-h-screen bg-gray-50 font-sans">
                  <Navbar />
                  <Routes>
                      <Route path="/" element={<FridgePage />} />
                      <Route path="/recipes" element={<RecipesPage />} />
                      <Route path="/recipe/:title" element={<RecipeDetailPage />} />
                      <Route path="/preferences" element={<PreferencesPage />} />
                      <Route path="/login" element={<LoginPage />} />
                      <Route path="/profile" element={<ProfilePage />} />
                      <Route path="/shopping-list" element={<ShoppingListPage />} />
                  </Routes>
              </div>
          </Router>
        </RecipeProvider>
        </ShoppingListProvider>
      </FridgeProvider>
    </AuthProvider>
  );
};

export default App;