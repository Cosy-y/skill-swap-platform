// my api file for talking to the backend
// this connects my html pages to the python api

// backend url - need to change when i put this online
const API_BASE_URL = 'http://localhost:8000';

// keeping track of logged in user
let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;
let authToken = localStorage.getItem('authToken') || null;

// API helper class - probably overkill but whatever
class SkillSwapAPI {
    
    // basic function to call the API
    async makeRequest(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultHeaders = {
            'Content-Type': 'application/json',
        };
        
        // add token if user is logged in
        if (authToken) {
            defaultHeaders['Authorization'] = `Bearer ${authToken}`;
        }
        
        const config = {
            headers: defaultHeaders,
            ...options,
            headers: { ...defaultHeaders, ...options.headers }
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'something broke');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    // login/signup stuff
    async register(userData, password) {
        const response = await this.makeRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                ...userData,
                password: password
            })
        });
        return response;
    }
    
    async login(email, password) {
        const response = await this.makeRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (response.token) {
            authToken = response.token;
            currentUser = response.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
        }
        
        return response;
    }
    
    async logout() {
        if (currentUser) {
            await this.makeRequest('/auth/logout', {
                method: 'POST',
                body: JSON.stringify({ user_id: currentUser.id })
            });
        }
        
        authToken = null;
        currentUser = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
    }
    
    // User endpoints
    async getPublicUsers(search = '', skill = '', location = '', limit = 20) {
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (skill) params.append('skill', skill);
        if (location) params.append('location', location);
        params.append('limit', limit);
        
        return await this.makeRequest(`/users/public?${params}`);
    }
    
    async getUserProfile(userId) {
        return await this.makeRequest(`/users/${userId}`);
    }
    
    async updateUserProfile(userId, userData) {
        return await this.makeRequest(`/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }
    
    async searchUsers(query, limit = 20) {
        const params = new URLSearchParams();
        params.append('query', query);
        params.append('limit', limit);
        
        return await this.makeRequest(`/users/search?${params}`);
    }
    
    // Swap endpoints
    async createSwapRequest(swapData, requesterId) {
        const params = new URLSearchParams();
        params.append('requester_id', requesterId);
        
        return await this.makeRequest(`/swaps/?${params}`, {
            method: 'POST',
            body: JSON.stringify(swapData)
        });
    }
    
    async getUserSwaps(userId, status = null, asRequester = null, limit = 50) {
        const params = new URLSearchParams();
        if (status) params.append('status', status);
        if (asRequester !== null) params.append('as_requester', asRequester);
        params.append('limit', limit);
        
        return await this.makeRequest(`/swaps/user/${userId}?${params}`);
    }
    
    async updateSwapStatus(swapId, status, message = null, userId) {
        const params = new URLSearchParams();
        params.append('user_id', userId);
        
        return await this.makeRequest(`/swaps/${swapId}?${params}`, {
            method: 'PUT',
            body: JSON.stringify({ status, message })
        });
    }
    
    async deleteSwapRequest(swapId, userId) {
        const params = new URLSearchParams();
        params.append('user_id', userId);
        
        return await this.makeRequest(`/swaps/${swapId}?${params}`, {
            method: 'DELETE'
        });
    }
    
    async getPendingSwapsCount(userId) {
        return await this.makeRequest(`/swaps/pending/count/${userId}`);
    }
    
    // Review endpoints
    async createReview(reviewData, reviewerId) {
        const params = new URLSearchParams();
        params.append('reviewer_id', reviewerId);
        
        return await this.makeRequest(`/reviews/?${params}`, {
            method: 'POST',
            body: JSON.stringify(reviewData)
        });
    }
    
    async getUserReviews(userId, limit = 20) {
        const params = new URLSearchParams();
        params.append('limit', limit);
        
        return await this.makeRequest(`/reviews/user/${userId}?${params}`);
    }
    
    async getSwapReviews(swapId) {
        return await this.makeRequest(`/reviews/swap/${swapId}`);
    }
    
    // Helper functions for the UI
    isLoggedIn() {
        return currentUser !== null && authToken !== null;
    }
    
    getCurrentUser() {
        return currentUser;
    }
    
    redirectToLogin() {
        window.location.href = 'index.html';
    }
    
    redirectToHome() {
        window.location.href = 'home.html';
    }
    
    // format rating stars
    formatRating(rating) {
        if (!rating) return '*****';
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '*'.repeat(fullStars);
        if (hasHalfStar) stars += '+';
        stars += '-'.repeat(5 - Math.ceil(rating));
        return stars;
    }
    
    // format dates nicely
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
    
    // show success/error messages
    showMessage(message, type = 'info') {
        // create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            max-width: 300px;
            background-color: ${type === 'success' ? '#059669' : type === 'error' ? '#dc2626' : '#1e3a8a'};
        `;
        
        document.body.appendChild(toast);
        
        // remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// create global API instance
const api = new SkillSwapAPI();

// check if user is logged in on page load
document.addEventListener('DOMContentLoaded', function() {
    // if on login page and already logged in, redirect to home
    if (window.location.pathname.includes('index.html') && api.isLoggedIn()) {
        api.redirectToHome();
    }
    
    // if not on login page and not logged in, redirect to login
    if (!window.location.pathname.includes('index.html') && !api.isLoggedIn()) {
        api.redirectToLogin();
    }
    
    // update navigation with user info
    updateNavigation();
});

function updateNavigation() {
    const user = api.getCurrentUser();
    if (user) {
        // update any user info in navigation
        const userNameElements = document.querySelectorAll('.user-name');
        userNameElements.forEach(el => el.textContent = user.name);
        
        const userPhotoElements = document.querySelectorAll('.user-photo');
        userPhotoElements.forEach(el => {
            if (user.profile_photo_url) {
                el.src = user.profile_photo_url;
            }
        });
    }
}

// handle logout
function handleLogout() {
    api.logout().then(() => {
        api.redirectToLogin();
    });
}
