// import React, { useState } from 'react';
// import axios from 'axios';
// import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
// import { GoogleOAuthProvider } from '@react-oauth/google'; // Import GoogleOAuthProvider
// import Login from './components/Login/Login';
// import "./App.css";
//
// function App() {
//     const [isAuthenticated, setIsAuthenticated] = useState(false);
//
//     const [imageSrc, setImageSrc] = useState('');
//     const [selectedFolder, setSelectedFolder] = useState(null);
//     const [brightness, setBrightness] = useState(50);
//     const [contrast, setContrast] = useState(50);
//     const [opacity, setOpacity] = useState(100);
//     const [red, setRed] = useState(100);
//     const [green, setGreen] = useState(100);
//     const [blue, setBlue] = useState(100);
//
//     const handleLogin = () => {
//         setIsAuthenticated(true);
//     };
//
//     const handleFolderChange = (event) => {
//         setSelectedFolder(event.target.files[0]);
//     };
//
//     const handleUpload = async () => {
//         if (!selectedFolder) {
//             alert('Please select a folder first.');
//             return;
//         }
//
//         const formData = new FormData();
//         formData.append('folder', selectedFolder);
//
//         try {
//             const response = await axios.post('http://localhost:5000/render', formData, {
//                 responseType: 'blob',
//                 headers: {
//                     'Content-Type': 'multipart/form-data',
//                 },
//             });
//             const imageUrl = URL.createObjectURL(response.data);
//             setImageSrc(imageUrl);
//         } catch (error) {
//             console.error('Error uploading file:', error);
//         }
//     };
//
//     const handleSliderChange = (event, setter) => {
//         setter(event.target.value);
//     };
//
//     const getImageFilterStyle = () => {
//         return {
//             filter: `brightness(${brightness}%) contrast(${contrast}%) opacity(${opacity}%)`,
//             backgroundColor: `rgba(${red}, ${green}, ${blue}, ${opacity / 100})`
//         };
//     };
//
//     return (
//         <GoogleOAuthProvider clientId="1059055942867-jvakpfolck2tamo8qp0p72ma7rs9d6vd.apps.googleusercontent.com"> {/* Thay YOUR_GOOGLE_CLIENT_ID bằng Client ID của bạn */}
//             <Router>
//                 <div className="App">
//                     <Routes>
//                         <Route
//                             path="/login"
//                             element={isAuthenticated ? <Navigate to="/" /> : <Login onLogin={handleLogin} />}
//                         />
//                         <Route
//                             path="/"
//                             element={isAuthenticated ? (
//                                 <div>
//                                     <header className="App-header">
//                                         <div className="side-panel">
//                                              <div className="upload-container">
//                         <input
//                             type="file"
//                             webkitdirectory=""
//                             mozdirectory=""
//                             directory=""
//                             onChange={handleFolderChange}
//                         />
//                         <button onClick={handleUpload}>Open</button>
//                     </div>
//                     <div className="slider-container">
//                         <div className="slider-group">
//                             <label>Brightness</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="100"
//                                 value={brightness}
//                                 onChange={(e) => handleSliderChange(e, setBrightness)}
//                             />
//                         </div>
//                         <div className="slider-group">
//                             <label>Contrast</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="100"
//                                 value={contrast}
//                                 onChange={(e) => handleSliderChange(e, setContrast)}
//                             />
//                         </div>
//                         <div className="slider-group">
//                             <label>Opacity</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="100"
//                                 value={opacity}
//                                 onChange={(e) => handleSliderChange(e, setOpacity)}
//                             />
//                         </div>
//                         <div className="slider-group">
//                             <label>Red</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="255"
//                                 value={red}
//                                 onChange={(e) => handleSliderChange(e, setRed)}
//                             />
//                         </div>
//                         <div className="slider-group">
//                             <label>Green</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="255"
//                                 value={green}
//                                 onChange={(e) => handleSliderChange(e, setGreen)}
//                             />
//                         </div>
//                         <div className="slider-group">
//                             <label>Blue</label>
//                             <input
//                                 type="range"
//                                 min="0"
//                                 max="255"
//                                 value={blue}
//                                 onChange={(e) => handleSliderChange(e, setBlue)}
//                             />
//                         </div>
//                     </div>
//                 </div>
//                 <div className="main-panel">
//                     {imageSrc && (
//                         <img
//                             src={imageSrc}
//                             alt="3D Render"
//                             className="render-image"
//                             style={getImageFilterStyle()}
//                         />
//                     )}
//                     {imageSrc && <div className="info-bar">Non Diagnostic Use Only</div>}
//                 </div>
//                                     </header>
//                                 </div>
//                             ) : (
//                                 <Navigate to="/login"/>
//                             )}
//                         />
//                     </Routes>
//                 </div>
//             </Router>
//         </GoogleOAuthProvider>
//     );
// }
//
// export default App;





















import React, { useState } from 'react';
import axios from 'axios';
import "./App.css";

function App() {
    const [imageSrc, setImageSrc] = useState('');
    const [selectedFolder, setSelectedFolder] = useState(null);
    const [opacity, setOpacity] = useState(100);
    const [red, setRed] = useState(1.0);
    const [green, setGreen] = useState(1.0);
    const [blue, setBlue] = useState(1.0);
    const [density, setDensity] = useState(1.0);

    const handleFolderChange = (event) => {
        const folder = event.target.files[0].webkitRelativePath.split('/')[0];
        setSelectedFolder(folder);
    };

    const handleUpload = async () => {
        if (!selectedFolder) {
            alert('Please select a folder first.');
            return;
        }

        const formData = new FormData();
        formData.append('folder', selectedFolder);  // Gửi tên thư mục

        try {
            const response = await axios.post('http://localhost:5000/render', formData, {
                responseType: 'blob',
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            const imageUrl = URL.createObjectURL(response.data);
            setImageSrc(imageUrl);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };


    const handleSliderChange = async (event, setter, sliderName) => {
        const value = event.target.value;
        setter(value);

        try {
            await axios.post('http://localhost:5000/update-sliders', {
                [sliderName]: value
            });
            handleUpload();  // Re-render the image with new settings
        } catch (error) {
            console.error('Error updating sliders:', error);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <div className="side-panel">
                    <div className="upload-container">
                        <input
                            type="file"
                            webkitdirectory=""
                            mozdirectory=""
                            directory=""
                            onChange={handleFolderChange}
                        />
                        <button onClick={handleUpload}>Open</button>
                    </div>
                    <div className="slider-container">
                        <div className="slider-group">
                            <label>Opacity</label>
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={opacity}
                                onChange={(e) => handleSliderChange(e, setOpacity, 'opacity')}
                            />
                        </div>
                        <div className="slider-group">
                            <label>Red</label>
                            <input
                                type="range"
                                min="0"
                                max="255"
                                value={red}
                                onChange={(e) => handleSliderChange(e, setRed, 'red')}
                            />
                        </div>
                        <div className="slider-group">
                            <label>Green</label>
                            <input
                                type="range"
                                min="0"
                                max="255"
                                value={green}
                                onChange={(e) => handleSliderChange(e, setGreen, 'green')}
                            />
                        </div>
                        <div className="slider-group">
                            <label>Blue</label>
                            <input
                                type="range"
                                min="0"
                                max="255"
                                value={blue}
                                onChange={(e) => handleSliderChange(e, setBlue, 'blue')}
                            />
                        </div>
                        <div className="slider-group">
                            <label>Density</label>
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={density}
                                onChange={(e) => handleSliderChange(e, setDensity, 'density')}
                            />
                        </div>
                    </div>
                </div>
                <div className="image-container">
                    {imageSrc && <img src={imageSrc} alt="DICOM visualization" />}
                </div>
            </header>
        </div>
    );
}

export default App;

