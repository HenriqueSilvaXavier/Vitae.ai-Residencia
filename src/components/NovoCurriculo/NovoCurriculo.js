import React, { useState } from 'react';
import ProgressBar from '../../imagens/progress-bar.svg';
import BeforeUploadFile from '../../imagens/before-upload-file.svg';
import AfterUploadFile from '../../imagens/after-upload-file.svg';
import AfterErrorFile from '../../imagens/after-error-file.svg';
import styles from './NovoCurriculo.module.css';
import successIcon from '../../imagens/successIcon.svg';
import errorIcon from '../../imagens/ErroIcon.svg';
import Caret from '../../imagens/caret-forward-outline 2.svg';

const NovoCurriculo = () => {
  const [currentFile, setCurrentFile] = useState(BeforeUploadFile);
  const [fileName, setFileName] = useState("");
  const [isButtonVisible, setIsButtonVisible] = useState(false);
  const [showSuccessNotification, setShowSuccessNotification] = useState(false);
  const [showErrorNotification, setShowErrorNotification] = useState(false);
  const [showPdfImage, setShowPdfImage] = useState(false);
  const [fileUrl, setFileUrl] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [isGenerateVisible, setIsGenerateVisible] = useState(false);

  const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload_resume', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setCurrentFile(AfterUploadFile);
        setFileName(file.name);
        setFeedback(data.feedback);
        setShowSuccessNotification(true);
        setShowErrorNotification(false);
        setIsButtonVisible(true);

        const fileURL = URL.createObjectURL(file);
        setFileUrl(fileURL);
      } else {
        throw new Error(data.error || "Erro no processamento do currículo.");
      }
    } catch (error) {
      setCurrentFile(AfterErrorFile);
      setShowErrorNotification(true);
      setShowSuccessNotification(false);
      console.error("Erro ao enviar o arquivo:", error);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    if (file && allowedTypes.includes(file.type)) {
      uploadResume(file);
    } else {
      setCurrentFile(AfterErrorFile);
      setShowErrorNotification(true);
    }
  };

  const handleCloseNotification = () => {
    setShowSuccessNotification(false);
  };

  const handleCloseError = () => {
    setShowErrorNotification(false);
  };

  const handleNextClick = () => {
    setShowPdfImage(true);
    setIsGenerateVisible(true);
  };

  const handleGenerateClick = () => {
    setShowPdfImage(false);
    setIsGenerateVisible(false);
    setShowSuccessNotification(false);
    setShowErrorNotification(false);
    setCurrentFile(BeforeUploadFile);
    setFileName("");
    setFeedback(null);
    setIsButtonVisible(false);
  };

  const formatFeedbackText = (text) => {
    return text
      .replace(/"/g, '')
      .split('\n')
      .slice(1, -1)
      .map((item, index) => {
        const [topic, rawDescription] = item.split(':');
        const description = rawDescription?.replace('.,', '.'); // Certifique-se de lidar com valores undefined
        const isDetail = topic.includes('_detail');
        return (
          <p key={index} className={styles.paragraph}>
            <img src={Caret} className={styles.CaretIcon} alt="Caret icon" />
            <strong>{topic}</strong>: {description}
          </p>
        );
      });
  };
  
  

  return (
    <div style={{ margin: '20px', width: '70%' }}>
      {showSuccessNotification && (
        <div className={styles.notification}>
          <img
            style={{ cursor: 'pointer', margin: '20px' }}
            src={successIcon}
            alt="Símbolo de sucesso"
          />
          <span>Sucesso. Currículo importado com sucesso.</span>
          <span className={styles.notificationClose} onClick={handleCloseNotification}>
            X
          </span>
        </div>
      )}

      {showErrorNotification && (
        <div className={styles.notificationError}>
          <img
            style={{ cursor: 'pointer', margin: '20px' }}
            src={errorIcon}
            alt="Símbolo de erro"
          />
          <span>Erro! Formato de arquivo inválido. Apenas PDF e DOCX são permitidos.</span>
          <span className={styles.notificationClose} onClick={handleCloseError}>
            X
          </span>
        </div>
      )}

      <div style={{ margin: '20px', textAlign: 'left' }}>
        <h1 style={{ color: 'white' }}>Novo Currículo</h1>
        <p style={{ color: 'white' }}>Siga o passo a passo para otimizar o seu currículo</p>
      </div>

      {!showPdfImage && (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <div className="uploadContainer" style={{ width: '57%', margin: 'auto' }}>
            <img src={ProgressBar} alt="Progresso" />
            <p style={{ color: 'white', textAlign: 'left', marginTop: 5 }}>1. Importar</p>

            <label htmlFor="fileInput">
              <img
                style={{ cursor: 'pointer', margin: '50px' }}
                src={currentFile}
                alt="Imagem de Upload"
              />
            </label>
            <input
              id="fileInput"
              type="file"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />

            {fileName && (
              <p className={styles.FileName} style={{ color: 'white', textAlign: 'center', marginTop: '10px', fontSize: '2em' }}>{fileName}</p>
            )}
          </div>
        </div>
      )}

      {showPdfImage && fileUrl && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <embed src={fileUrl} type="application/pdf" width="39%" height="450px" style={{ marginRight: '20px' }} />
          
          <div className={styles.feedback} style={{ width: '48%' }}>
            {typeof feedback === "object" ? (
              <ul>
                {Object.entries(feedback).map(([key, value], index) => (
                  <li key={index}>
                    <strong style={{ color: "purple" }}>{key}:</strong> {JSON.stringify(value)}
                  </li>
                ))}
              </ul>
            ) : (
              <p>
                {formatFeedbackText(feedback)}
              </p>
            )}
          </div>
        </div>
      )}

      {isGenerateVisible && (
        <div className={styles.main_container_proximo_btn}>
          <button className={styles.proximo_btn} onClick={handleGenerateClick}>Gerar novamente</button>
        </div>
      )}

      {isButtonVisible && !showPdfImage && (
        <div className={styles.main_container_proximo_btn}>
          <button className={styles.proximo_btn} onClick={handleNextClick}>Próximo</button>
        </div>
      )}
    </div>
  );
};

export default NovoCurriculo;
